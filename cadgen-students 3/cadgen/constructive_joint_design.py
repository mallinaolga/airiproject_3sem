"""Rank multiple spatial layouts, true cylindrical fits and hardware designs."""

from dataclasses import asdict,replace
import random
import math
import cadquery as cq
import numpy as np

from generirovanie_pazov.generate_grooves import sample_profile,PROFILE_TYPES
from .assembly_geometry import (Connection,GeometryRejected,Split,build_groove,frame,
                                require_solid,validate_connection,difference_volume)
from .assembly_validation import transform_part,overlap_volume
from .adaptive_joints import contact_centers,material_depth
from .constructive_geometry import general_contact,positive_depth,box_bounds,face_chord
from .constructive_fasteners import fasten
from .joint_design import make_joint,combine


def sized_profile(kind,width,depth):
    sample=sample_profile(random.Random('constructive:'+kind),kind)
    if kind=='round':
        depth=min(depth,width/2);return replace(sample,opening_width=2*depth,depth=depth,radius=depth)
    x=width/sample.max_width;z=depth/sample.depth
    return replace(sample,opening_width=sample.opening_width*x,depth=depth,
        bottom_width=sample.bottom_width*x if sample.bottom_width else None,
        neck_depth=sample.neck_depth*z if sample.neck_depth else None)


def _split(first,second,rotation,origin):
    local=lambda shape:transform_part(shape,rotation.T,-rotation.T@origin)
    return Split(local(first.fuse(second)),local(second),local(first),rotation,origin,{})


def _orient_planar(donor,receiver,face):
    n=np.array(face.normalAt().toTuple());origin=np.array(face.Center().toTuple())
    # General contact is oriented out of receiver when called in that order.
    rotation=frame(n)
    local_face=transform_part(face,rotation.T,-rotation.T@origin);b=local_face.BoundingBox()
    if b.xlen>b.ylen:
        rotation=rotation@np.array([[0.,-1.,0.],[1.,0.,0.],[0.,0.,1.]])
        local_face=transform_part(face,rotation.T,-rotation.T@origin)
    return _split(donor,receiver,rotation,origin),local_face


def _cylinder_frame(donor,receiver,description):
    axis=np.array(description['axis']);point=np.array(description['origin'])
    # Line/surface intersections locate the actual insertion mouth. The
    # receiver may have a curved outside surface, not an infinite plane.
    from .constructive_geometry import axis_intervals
    intervals=axis_intervals(receiver,point,axis)
    if not intervals:raise GeometryRejected('Cylinder axis misses receiver material')
    center=np.array(donor.Center().toTuple());projection=np.dot(center-point,axis)
    interval=min(intervals,key=lambda v:min(abs(projection-v[0]),abs(projection-v[1])))
    high_side=abs(projection-interval[1])<abs(projection-interval[0])
    normal=axis if high_side else -axis
    origin=point+axis*(interval[1] if high_side else interval[0])
    return _split(donor,receiver,frame(normal),origin)


def _grooves(split,face,layout,kind,geometry,design,depth_factor=1.):
    b=face.BoundingBox();w,l=b.xlen,b.ylen
    if min(w,l)<max(20*design.service_overlap,design.min_feature_size*3):
        raise GeometryRejected('Service-overlap ribbon is not a usable fastening interface')
    center=face.Center();cx,cy=center.x,center.y
    if layout=='four_pins':
        centers=[(cx+sx*w*.28,cy+sy*l*.28) for sx in (-1,1) for sy in (-1,1)]
        width,length=w*.16,l*.16
    elif layout=='two_end_pins':
        centers=[(cx,cy-l*.3),(cx,cy+l*.3)];width,length=w*.4,l*.16
    elif layout=='two_long_grooves':
        centers=[(cx-w*.25,cy),(cx+w*.25,cy)];width,length=w*.16,l*.82
    elif layout=='one_central_pin':
        centers=[(cx,cy)];width,length=w*.22,min(l*.22,w*.55)
    else:
        centers=[(cx,cy)];width,length=w*.42,l*.82
    seeds=contact_centers(face,32)
    centers=[p if face.distance(cq.Vertex.makeVertex(*p,0.))<1e-7 else
             min((q for q,_ in seeds),key=lambda q:((q[0]-p[0])/w)**2+((q[1]-p[1])/l)**2) for p in centers]
    if len(set(centers))!=len(centers):raise GeometryRejected('Distributed centers collapse on trimmed contact')
    donor,receiver=split.upper,split.lower;voids=[];features=[];zones=[]
    directions=None
    for x,y in centers:
        if face.distance(cq.Vertex.makeVertex(x,y,0.))>1e-7:
            raise GeometryRejected('Distributed feature center leaves the actual trimmed contact')
        rd=material_depth(receiver,(x,y),(0,0,-1));dd=material_depth(donor,(x,y),(0,0,1))
        chord_x=face_chord(face,(x,y),0);chord_y=face_chord(face,(x,y),1)
        local_width=min(width,chord_x*.65);local_length=min(length,chord_y*.85)
        depth=min(rd*.3,dd*.5,w*.3)*depth_factor
        selected=sized_profile(kind,local_width,depth)
        if min(selected.opening_width,selected.depth,local_length)<design.min_feature_size:
            raise GeometryRejected('Feature below explicit design floor; no microscopic retry')
        gap=min(geometry.clearance,.025*min(selected.opening_width,selected.depth,local_length))
        local_geometry=replace(geometry,clearance=gap)
        current=replace(split,original=donor.fuse(receiver),upper=donor,lower=receiver)
        result=build_groove(current,random.Random(42),local_geometry,kind,centers=[(x,y)],
            footprint=dict(width=local_width,depth=depth,length=local_length,anchor_depth=dd*.3),
            adaptive=True,exact_profile=selected)
        donor,receiver=[s for _,s in result.components[:2]];voids.append(result.removed)
        features.append(result.parameters)
        margin=result.parameters['local_material_margin']
        # Only the actual groove corridor is protected, not the large empty
        # rectangle spanning several independent features.
        zmin=-selected.depth-gap-margin
        yhalf=result.parameters['tool_length']/2+gap+margin
        zones.append([x-selected.max_width/2-gap-margin,y-yhalf,zmin,
                      x+selected.max_width/2+gap+margin,y+yhalf,min(dd*.3,margin)])
        directions=result.paths[0][2]
    removed=combine(voids)
    if difference_volume(split.original.cut(donor.fuse(receiver)),removed)>geometry.volume_tolerance:
        raise GeometryRejected('Multiple groove void recipes disagree')
    return Connection([('part_1',donor),('part_2',receiver)],removed,
        dict(type='distributed_grooves',layout=layout,depth_variant=depth_factor,features=features,feature_count=len(features),
             clearance=max(f['clearance'] for f in features),feature_zones_local=zones,
             length_selected_independently=True,mechanical_retention_checked=False),
        [('part_1',['part_2'],directions)])


def cylindrical_fit(split,pin_radius,geometry,design,*,crossed=False,depth_scale=1.):
    rd=positive_depth(split.lower,[0,0,0],(0,0,-1));dd=positive_depth(split.upper,[0,0,0],(0,0,1))
    if min(rd,dd)<=0:raise GeometryRejected('No connected donor and receiver material on fit axis')
    radius=pin_radius if crossed else pin_radius*.65
    floor=max(design.min_feature_size,.15*radius)
    depth=min(rd-floor,rd*.85) if crossed else min(rd*.65,2*radius)
    depth*=depth_scale
    gap=min(geometry.clearance,.025*radius)
    if min(radius,depth)<design.min_feature_size:raise GeometryRejected('Cylindrical fit below design scale')
    envelope=cq.Solid.makeCylinder(radius+gap+floor,depth*.55,cq.Vector(0,0,-depth*.85))
    if envelope.cut(split.lower).Volume()>geometry.volume_tolerance:
        raise GeometryRejected('Socket lacks actual side material around its buried engagement')
    anchor=cq.Solid.makeCylinder(radius*.85,min(dd*.2,radius*.3),cq.Vector(0,0,0))
    if anchor.cut(split.upper).Volume()>geometry.volume_tolerance:
        raise GeometryRejected('Fit is supported only by a narrow contact trace, not a bulk donor anchor')
    pin=cq.Solid.makeCylinder(radius,depth,cq.Vector(0,0,-depth))
    cavity=cq.Solid.makeCylinder(radius+gap,depth+gap+.001,cq.Vector(0,0,-depth-gap))
    tongue=require_solid(pin.intersect(split.lower).clean(),'cylindrical tongue')
    donor=require_solid(split.upper.fuse(tongue).clean(),'cylindrical donor')
    receiver=require_solid(split.lower.cut(cavity).clean(),'cylindrical socket')
    if difference_volume(donor.cut(split.upper),tongue)>geometry.volume_tolerance:
        raise GeometryRejected('Cylindrical tongue lost in Boolean transfer')
    # Actual support behind the socket floor, not global receiver bbox depth.
    probe=[0.,0.,-depth-gap]
    residual=positive_depth(receiver,probe,(0,0,-1))
    if residual<floor*.9:raise GeometryRejected('Insufficient actual socket floor')
    removed=split.lower.intersect(cavity).cut(tongue)
    feature=dict(type='cylindrical_fit',pin_radius=radius,hole_radius=radius+gap,depth=depth,
        clearance=gap,coaxial=True,receiver_axis_depth=rd,actual_axis_floor=residual,
        crossed_axes=crossed,full_cylinder_not_round_profile=True,remaining_unfixed_dof=['axial_withdrawal','rotation_about_axis'])
    zone=[-radius-gap-floor,-radius-gap-floor,-depth-gap-floor,radius+gap+floor,radius+gap+floor,min(dd*.3,floor)]
    return Connection([('part_1',donor),('part_2',receiver)],removed,
        dict(type='cylindrical_fit',features=[feature],feature_count=1,clearance=gap,
             feature_zones_local=[zone],local_material_margin=floor),
        [('part_1',['part_2'],[(0,0,1)])])


def _transverse(split,fit,geometry,design,diameter):
    # Drill perpendicular to the insertion axis, at half the inserted depth.
    feature=fit.parameters['features'][0];depth=feature['depth']
    origin=np.array([0.,0.,-depth*.5]);r=frame([1.,0.,0.])
    donor,receiver=[s for _,s in fit.components[:2]]
    local=lambda s:transform_part(s,r.T,-r.T@origin)
    current=Split(local(donor.fuse(receiver)),local(receiver),local(donor),np.eye(3),np.zeros(3),{})
    hardware=fasten(current,[(0.,0.)],diameter,geometry,design,'bolted')
    moved=[(n,transform_part(s,r,origin)) for n,s in hardware.components]
    paths=[fit.paths[0]]
    for n,fixed,dirs in hardware.paths[1:]:paths.append((n,fixed,[tuple(r@np.asarray(d)) for d in dirs]))
    # Store individual hardware directions: the fastener axis differs from
    # the insertion axis and must never be silently treated as a Z bolt.
    hardware_directions={n:[list(r@np.asarray(d)) for d in dirs] for n,_,dirs in hardware.paths[1:]}
    feature_zones=list(fit.parameters['feature_zones_local'])
    for bounds in hardware.parameters['feature_zones_local']:
        box=cq.Solid.makeBox(bounds[3]-bounds[0],bounds[4]-bounds[1],bounds[5]-bounds[2],cq.Vector(*bounds[:3]))
        feature_zones.append(box_bounds(transform_part(box,r,origin),0.))
    return Connection(moved,combine([fit.removed,transform_part(hardware.removed,r,origin)]),
        dict(type='cylindrical_fit_transverse_bolt',features=[*fit.parameters['features'],
             *[dict(f,fastener_to_joint_rotation=r.tolist(),fastener_origin_in_joint=origin.tolist()) for f in hardware.parameters['features']]],
             feature_count=1+hardware.parameters['feature_count'],bolts=hardware.parameters['bolts'],screws=0,
             feature_zones_local=feature_zones,hardware_directions_local=hardware_directions),paths)


def _score(result,face_area,spread):
    features=result.parameters['features'];kind=result.parameters['type']
    coverage=0.
    for feature in features:
        if feature['type']=='groove':
            p=feature['profile'];coverage+=max(p['opening_width'],p.get('bottom_width') or 0)*feature['central_engagement_length']
        elif feature['type']=='cylindrical_fit':coverage+=np.pi*feature['pin_radius']**2
        else:coverage+=feature['shaft_diameter']**2*2
    distributed=min(1.,coverage/max(face_area,1e-6))
    # These are interpretable geometric preferences, not a strength calculation.
    score=5*distributed+spread+(.8 if len(features)>1 else 0)
    if kind.startswith('cylindrical_fit'):score+=4
    if kind=='cylindrical_fit_transverse_bolt':score+=1.5
    if result.parameters.get('layout')=='four_pins':score+=1.
    if result.parameters.get('layout')=='two_long_grooves':score+=1.5
    return float(score),dict(engagement_area_fraction=distributed,distribution_score=spread,
        geometric_anti_rotation_heuristic=len(features)>1,mechanical_strength_checked=False,
        movement_constraints='geometric layout heuristic, not a load or force-closure proof')


def propose_constructive(raw,a,b,descriptions,geometry,design,*,only=None,profile=None):
    design.validate();patch=general_contact(raw[b],raw[a]);options=[];rejected=[];attempts=0
    if not patch.Faces():raise GeometryRejected('No actual shared B-rep surface')
    name='j_'+a+'_'+b
    role_start=0;role_budget=max(1,(design.max_designs_per_pair-4)//2);role_limited=True
    def accept(split,owners,result,spread,description):
        score,scoring=_score(result,patch.Area(),spread)
        joint=make_joint(split,result,owners,name,score,dict(description,scoring=scoring),geometry)
        joint.score=score
        custom=result.parameters.get('hardware_directions_local',{})
        if custom:
            joint.parameters['hardware_directions_world']={name+'_'+n:[(split.rotation@np.asarray(d)).tolist() for d in dirs]
                                                           for n,dirs in custom.items()}
        options.append(joint)
    def attempt(label,split,owners,builder,spread=0.,description=None):
        nonlocal attempts
        if attempts>=design.max_designs_per_pair or (role_limited and attempts-role_start>=role_budget):return
        attempts+=1
        try:accept(split,owners,builder(),spread,dict(description or {},design=label))
        except Exception as error:rejected.append(dict(design=label,reason=f'{type(error).__name__}: {error}'))
    for donor,receiver in ((a,b),(b,a)):
        role_start=attempts
        desc=descriptions.get(donor,{})
        cyl=desc.get('cylinder')
        receiver_cyl=descriptions.get(receiver,{}).get('cylinder')
        if cyl:
            try:
                split=_cylinder_frame(raw[donor],raw[receiver],cyl)
                crossed=bool(receiver_cyl and abs(np.dot(cyl['axis'],receiver_cyl['axis']))<.95)
                if only in (None,'cylindrical_fit') and not crossed:
                    for depth_scale in (1.,.55):
                        attempt('cylindrical_fit',split,(donor,receiver),
                            lambda depth_scale=depth_scale:cylindrical_fit(split,cyl['radius'],geometry,design,depth_scale=depth_scale),1)
                if only in (None,'cylindrical_fit_transverse_bolt'):
                    attempt('cylindrical_fit_transverse_bolt',split,(donor,receiver),
                        lambda:_transverse(split,cylindrical_fit(split,cyl['radius'],geometry,design,crossed=crossed),
                                           geometry,design,max(design.min_feature_size,cyl['radius']*.3)),1.5)
            except Exception as error:rejected.append(dict(design='cylinder_axis',reason=str(error)))
        contacts=general_contact(raw[receiver],raw[donor])
        planar=sorted([f for f in contacts.Faces() if f.geomType()=='PLANE'],key=lambda f:-f.Area())
        for face in planar[:3]:
            split,local_face=_orient_planar(raw[donor],raw[receiver],face);bb=local_face.BoundingBox()
            if min(bb.xlen,bb.ylen)<max(20*design.service_overlap,design.min_feature_size*3):
                rejected.append(dict(design='planar_interface',reason='service-overlap ribbon; no microscopic fastening'))
                continue
            long=bb.ylen/max(bb.xlen,1e-9)>2.5
            layouts=['two_long_grooves','one_long_groove','two_end_pins','one_central_pin'] if long else ['four_pins','two_end_pins','one_long_groove','one_central_pin']
            if only in (None,*layouts):
                for layout in layouts:
                    if only and layout!=only:continue
                    for kind in ([profile] if profile else PROFILE_TYPES):
                        attempt(layout+'/'+kind,split,(donor,receiver),
                            lambda layout=layout,kind=kind:_grooves(split,local_face,layout,kind,geometry,design),
                            1.5 if layout in ('four_pins','two_long_grooves') else .5)
                        if kind=='rectangular':
                            attempt(layout+'/'+kind+'/shallower',split,(donor,receiver),
                                lambda layout=layout,kind=kind:_grooves(split,local_face,layout,kind,geometry,design,.55),
                                1.5 if layout in ('four_pins','two_long_grooves') else .5)
            if only in (None,'bolted','self_tapping_screw'):
                for count in (4,2,1):
                    center=local_face.Center();x,y=center.x,center.y
                    centers=([(x+sx*bb.xlen*.28,y+sy*bb.ylen*.28) for sx in (-1,1) for sy in (-1,1)] if count==4
                             else [(x,y-bb.ylen*.3),(x,y+bb.ylen*.3)] if count==2 else [(x,y)])
                    seeds=contact_centers(local_face,32)
                    if not seeds:continue
                    centers=[p if local_face.distance(cq.Vertex.makeVertex(*p,0))<1e-7 else
                             min((q for q,_ in seeds),key=lambda q:np.linalg.norm(np.array(q)-p)) for p in centers]
                    if len(set(centers))!=len(centers):continue
                    boundary=cq.Compound.makeCompound(local_face.Wires())
                    radius=min(boundary.distance(cq.Vertex.makeVertex(*p,0.)) for p in centers)
                    diameter=min(bb.xlen*.08,bb.ylen*.08,5.,radius*.6)
                    if diameter<design.min_feature_size:continue
                    for kind in ('bolted','self_tapping_screw'):
                        if only and only!=kind:continue
                        attempt(kind+f'/{count}',split,(donor,receiver),
                            lambda kind=kind:fasten(split,centers,diameter,geometry,design,kind),1.5 if count==4 else .7)
    # Curved prism/cylinder attachments may have no planar face. A normal
    # cylindrical boss is still a real cylinder, not a round profile channel.
    role_limited=False
    if (not all(descriptions.get(n,{}).get('cylinder') for n in (a,b))
            and any(f.geomType()!='PLANE' for f in patch.Faces()) and only in (None,'cylindrical_fit')):
        face=max([f for f in patch.Faces() if f.geomType()!='PLANE'],key=lambda f:f.Area());u0,u1,v0,v1=face._uvBounds()
        normal,point=face.normalAt((u0+u1)/2,(v0+v1)/2)
        origin=np.array(point.toTuple());normal=np.array(normal.toTuple());split=_split(raw[a],raw[b],frame(normal),origin)
        for sign in (1,-1):
            if sign==-1:split=_split(raw[b],raw[a],frame(-normal),origin)
            owners=(a,b) if sign==1 else (b,a)
            radius=min(raw[a].BoundingBox().DiagonalLength,raw[b].BoundingBox().DiagonalLength)*.06
            attempt('curved_attachment_cylindrical_boss',split,owners,
                    lambda:cylindrical_fit(split,radius,geometry,design),.5)
    report=dict(attempts=attempts,limit=design.max_designs_per_pair,valid_designs=len(options),
                rejected=rejected,exhaustive=False,ranked_by_geometry=True,first_success_not_automatically_selected=True)
    if not options:
        error=GeometryRejected('No constructive joint within bounded design search');error.report=report;raise error
    options.sort(key=lambda j:-j.score)
    # Retain geometric variety rather than filling the entire option budget
    # with identical profiles from the same distributed layout.
    selected=[];groups={}
    for option in options:
        signature=(option.parameters['type'],option.parameters.get('layout'))
        groups.setdefault(signature,[]).append(option)
    while groups and len(selected)<design.max_options_per_pair:
        for signature in list(groups):
            selected.append(groups[signature].pop(0))
            if not groups[signature]:del groups[signature]
            if len(selected)>=design.max_options_per_pair:break
    for option in selected:option.selection['constructive_search']=report
    return selected
