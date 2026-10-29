"""Proportional through bolts and blind screws with explicit shaft limits."""

from dataclasses import asdict
import math
import cadquery as cq

from Bolty import BoltSpec,build_bolt
from Gaiki import NutSpec,build_nut
from Otverstiya import through_hole_cutter
from .assembly_geometry import Connection,GeometryRejected,require_solid,difference_volume
from .assembly_validation import planar_contact_area
from .constructive_geometry import axis_intervals,positive_depth,box_bounds


def fasten(split,centers,diameter,geometry,design,kind='bolted'):
    """All main shapes are in a fastener frame; head withdraws along +Z.

    Small circular counterbores provide actual flat bearing seats on curved
    exterior surfaces. Screw retention is assumed, never proved by a smooth rod.
    """
    if kind not in ('bolted','self_tapping_screw'):raise ValueError(kind)
    upper,lower=split.upper,split.lower
    source=upper.fuse(lower)
    tools=[];hardware=[];paths=[('part_1',['part_2'],[(0,0,1)])];specs=[];zones=[]
    for index,(x,y) in enumerate(centers,1):
        material=axis_intervals(source,[x,y,0.],(0,0,1))
        if not material:raise GeometryRejected('No shaft material column')
        low,high=min(v[0] for v in material),max(v[1] for v in material)
        seat=.15*diameter
        top=high-seat
        gap=min(geometry.clearance,diameter*.025)
        head_width=diameter*1.8;head_height=.6*diameter;nut_height=.65*diameter;tip=.35*diameter
        head_radius=head_width/(2*math.cos(math.pi/6))
        if kind=='self_tapping_screw':
            # The second part is lower in this frame. Measure from the actual
            # interface; do not substitute total bolt/part length for engagement.
            donor_depth=positive_depth(upper,[x,y,0.],(0,0,1))
            receiver_depth=positive_depth(lower,[x,y,0.],(0,0,-1))
            engagement=max(design.min_screw_engagement,diameter*2)
            floor=max(diameter*.2,design.min_feature_size)
            if min(donor_depth,receiver_depth)<=0 or receiver_depth<engagement+floor:
                raise GeometryRejected('Blind screw lacks required second-part engagement and floor')
            bottom=-engagement;length=top-bottom
            nut_base=None
        else:
            bottom=low+seat;nut_base=bottom-nut_height
            length=top-bottom+nut_height+tip;engagement=None
        if length>design.max_shaft_length+1e-7:
            raise GeometryRejected(f'Shaft length {length:g} exceeds {design.max_shaft_length:g} mm')
        if length<=diameter:raise GeometryRejected('Insufficient axial bearing span')
        shaft_bottom=top-length
        hole_bottom=bottom if kind=='self_tapping_screw' else low-1
        hole=through_hole_cutter(diameter+2*gap,hole_bottom,high+1,(x,y))
        head_seat=cq.Solid.makeCylinder(head_radius+gap,high-top+head_height+1,cq.Vector(x,y,top))
        cutter=hole.fuse(head_seat)
        if kind=='bolted':
            nut_seat=cq.Solid.makeCylinder(head_radius+gap,bottom-low+1,cq.Vector(x,y,low-1))
            cutter=cutter.fuse(nut_seat)
        next_upper=require_solid(upper.cut(cutter).clean(),'fastened donor')
        next_lower=require_solid(lower.cut(cutter).clean(),'fastened receiver')
        spec=BoltSpec('hex_head',length,diameter,head_width,head_height,0.,0.)
        rod=build_bolt(spec,adaptive=True).translate((x,y,top))
        head_area=planar_contact_area(next_upper.fuse(next_lower),rod,1e-6)
        if head_area<.05*diameter**2:raise GeometryRejected('No accessible flat head bearing seat')
        name=('bolt_' if kind=='bolted' else 'screw_')+str(index)
        hardware.append((name,rod));paths.append((name,['part_1','part_2'],[(0,0,1)]))
        nut_spec=None;nut_area=None
        if kind=='bolted':
            nut_spec=NutSpec(diameter+2*gap,head_width,nut_height,.05*diameter)
            nut=build_nut(nut_spec,adaptive=True).translate((x,y,nut_base))
            nut_area=planar_contact_area(next_upper.fuse(next_lower),nut,1e-6)
            if nut_area<.05*diameter**2:raise GeometryRejected('No accessible flat nut bearing seat')
            hardware.append((f'nut_{index}',nut))
            paths.append((f'nut_{index}',['part_1','part_2',name],[(0,0,-1)]))
        else:
            # The blind cutter must remove ten (configurable) real mm of the
            # lower component, not ten mm of air or another constituent.
            probe=cq.Solid.makeCylinder((diameter+2*gap)/2,engagement,cq.Vector(x,y,-engagement))
            if probe.cut(lower).Volume()>geometry.volume_tolerance:
                raise GeometryRejected('Blind screw engagement crosses missing second-part material')
        specs.append(dict(type=kind,center_in_fastener_frame=[x,y,0.],shaft_diameter=diameter,
            shaft_length=length,max_shaft_length=design.max_shaft_length,clearance=gap,
            head_seat_z=top,lower_seat_z=bottom,head_bearing_area=head_area,nut_bearing_area=nut_area,
            bolt=asdict(spec),nut=asdict(nut_spec) if nut_spec else None,
            second_part_engagement_mm=engagement,min_screw_engagement=design.min_screw_engagement,
            blind=kind=='self_tapping_screw',threaded=False,retention_assumed=kind=='self_tapping_screw',
            thread_retention_proven=False,head_accessibility_requires_path_check=True))
        # A circular counterbore extends past the flats of a hexagonal head.
        # Protect its actual material removal as well as the hardware itself.
        protected=[rod,cutter.intersect(source),*([nut] if kind=='bolted' else [])]
        tools.append(cutter);zones.append(box_bounds(cq.Compound.makeCompound(protected),diameter*.1))
        upper,lower=next_upper,next_lower
    removed=source.cut(upper.fuse(lower))
    return Connection([('part_1',upper),('part_2',lower),*hardware],removed,
        dict(type=kind,features=specs,feature_count=len(specs),bolts=len(specs) if kind=='bolted' else 0,
             screws=len(specs) if kind!='bolted' else 0,threaded=False,feature_zones_local=zones),paths)
