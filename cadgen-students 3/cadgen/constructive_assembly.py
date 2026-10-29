"""Constructive joint ranking on an independent completed geometric partition."""

from dataclasses import replace
from .constructive_geometry import ConstructiveSettings,general_contact
from .constructive_joint_design import propose_constructive
from .decomposition import DecompositionSettings
from .decomposition_assembly import assemble_partition


def assemble_constructive(state,geometry,design=None,*,only=None,profile=None,edge_callback=None):
    design=design or ConstructiveSettings();design.validate()
    descriptions=state.checks.get('constructive_elements',{})
    if len(state.raw)==1:
        state.assembly=dict(status='single_component',success=True,partition_modified=False,trials=[])
        state.checks['graph']=dict(vertices=list(state.raw),contacts=[],selected_edges=[],connected=True)
        state.checks['assembly_sequence_checked']=True
        state.sequence=[dict(step=0,component=next(iter(state.raw)),action='place_base',stationary_components=[])]
        return state
    settings=replace(DecompositionSettings(),max_sequence_states=design.max_assembly_states,
                     max_connection_trials=design.max_options_per_pair)
    return assemble_partition(state,42,geometry,settings,edge_callback=edge_callback,
        contact_function=general_contact,incremental_validation=True,
        joint_search=lambda a,b:propose_constructive(state.raw,a,b,descriptions,geometry,design,only=only,profile=profile))
