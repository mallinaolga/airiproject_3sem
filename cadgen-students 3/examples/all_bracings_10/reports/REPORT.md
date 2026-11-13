# All bracings: ten CADGen inputs

Global installation order/trajectories were not checked.

| Model | Seed | Raw parts | Joints | Selected types | Result |
|---|---|---|---|---|---|
| 1 | 42 | — | 0 | — | decomposition: original: expected one valid positive-volume solid; source_valid=True, solids=2 |
| 2 | 17 | — | 0 | — | decomposition: original: expected one valid positive-volume solid; source_valid=True, solids=2 |
| 3 | 73 | — | 0 | — | decomposition: original: expected one valid positive-volume solid; source_valid=True, solids=2 |
| 4 | 101 | 4 | 3 | pinned: 1, mortise_tenon: 1, dovetail: 1 | geometry_verified; STEP/STL exported |
| 5 | 123 | 6 | 5 | bolted: 1, mortise_tenon: 1, dovetail: 1, bayonet: 1, pinned: 1 | geometry_verified; STEP/STL exported |
| 6 | 202 | 11 | 10 | mortise_tenon: 4, dovetail: 1, bayonet: 1, pinned: 1, bolted: 1, threaded: 1, snap_fit: 1 | geometry_verified; STEP/STL exported |
| 7 | 314 | 7 | 6 | mortise_tenon: 1, threaded: 1, dovetail: 1, pinned: 1, bolted: 1, tongue_groove_stop: 1 | geometry_verified; STEP/STL exported |
| 8 | 515 | 6 | 5 | mortise_tenon: 2, bolted: 1, dovetail: 1, pinned: 1 | geometry_verified; STEP/STL exported |
| 9 | 616 | 11 | 0 | — | assembly: No validated complete assembly of the fixed constituents within the search; technical_limit_reached, search_states=256 |
| 10 | 717 | 7 | 6 | bolted: 1, dovetail: 3, mortise_tenon: 1, pinned: 1 | geometry_verified; STEP/STL exported |

Selected joint coverage: {'pinned': 6, 'mortise_tenon': 10, 'dovetail': 8, 'bolted': 5, 'bayonet': 2, 'threaded': 2, 'snap_fit': 1, 'tongue_groove_stop': 1}
Missing types in the ten selected results: []

All rejected source attempts and candidate designs remain in JSON reports.
