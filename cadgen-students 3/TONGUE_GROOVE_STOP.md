# Longitudinal rectangular groove with stop

Request `--connection tongue_groove_stop` in `cadgen.assembly_generator`, with
either two-part splitting or automatic decomposition. Selection is explicit;
existing random/auto defaults are unchanged.

The builder reuses `build_groove` to make the integral rectangular tongue and
its anchor. It reuses `profile_prism` and `offset_prism` to open the receiver
only towards negative Y in the cut frame. The opposite end remains an integral
material wall. Insertion along positive Y ends in zero-gap bearing contact
between the tongue's leading face and this wall. Side/floor normal clearance
defaults to 0.2 mm and must satisfy `0 <= c < 1`. The stop is not a separate
component. This is neither a closed mortise nor an undercut dovetail/T-slot.

The full entrance channel must have the specified local floor/side material
margin, including a terminal wall at least `min_wall` thick. Curved or hollow
parts without that material envelope are conservatively rejected. Validation
checks actual leading-face contact, expected bodies, pairwise intersections,
source-material accounting, and positive-volume collision for small forward
overtravel probes. Existing path sampling checks withdrawal towards negative Y,
equivalently insertion from that side. Export retains the distinct `type` and
`joint_type`, stop dimensions, measured checks, and insertion direction.

Reverse extraction and lifting along positive Z remain possible. This is not
self-retaining, and the forward stop only constrains the stated movement at
the seated pose. Finite path/probe samples do not prove a continuous path,
global six-DOF fixation, or physical load capacity. STEP is roundtrip checked;
exploded positions are visualization placements, not installation trajectories.
