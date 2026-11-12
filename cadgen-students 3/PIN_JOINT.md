# Separate pin connection

Use `--connection pinned` with `cadgen.assembly_generator` in either the two-part
or automatic decomposition workflow. The existing automatic/random selection
defaults are unchanged; this type is explicitly requested.

`cadgen.pin_joint.build_pin` returns the shared `Connection`: two drilled bodies
and a separate `pin_1`. It uses `Otverstiya.through_hole_cutter` for coaxial
through holes. The existing `cylindrical_fit` remains an integral protrusion.
Diameter defaults to 4 mm and can be supplied to the Python builder. Pin length
equals the complete axial thickness of both bodies, with flush ends.

The radial clearance defaults to 0.2 mm and must satisfy `0 <= clearance < 1`.
The corresponding diametral clearance is twice the radial clearance. Full
material columns around each hole certify the requested local side-wall margin;
each engagement length must be at least `min_wall`. Voids, curved seats without
full columns, and inadequate side material are conservatively rejected.

Validation reconstructs both bores and the pin and compares actual BREP geometry,
then uses existing solid validity, collision, material-preservation and sampled
insertion checks. Export retains a separate pin solid, its role, STEP/STL files,
and insertion direction. `Joint` supplies the identifier and component owners.
Hardware withdrawal directions are transformed to world coordinates for the
existing assembly sequence checker. STEP is reimported by the existing exporter.

This clearance-fit pin has no head, interference fit, adhesive or axial retainer.
It limits transverse motion after clearance take-up but permits axial withdrawal
and rotation about its axis. Finite path samples do not certify continuous
collision freedom; no strength, friction or manufacturing-fit certification is
claimed. The decomposition algorithm and bolt generators are unchanged.
