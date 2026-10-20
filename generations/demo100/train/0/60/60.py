import cadquery as cq
from cadgen.selectors import PointOnEdgeSelector, PointOnFaceSelector
from cadgen.extrude import extrude
from cadgen.shell import shell
from cadgen.hole import hole
from cadgen.revolve import revolve
from cadgen.orto_cut import orto_cut
from cadgen.sweep import sweep
from cadgen.sweep_adv import sweep_adv
from cadgen.spring import spring
from cadgen.loft import loft
from cadgen.gear import gear
from cadgen.rib import rib
from cadgen.thread import thread
r = None
r=extrude(r, (0, 0, -22), 'XY', "sketch().arc((-52, -23), (47, 33), (-39, -41)).segment((-39, -38)).segment((-31, -38)).segment((-31, -23)).segment((-39, -23)).segment((-39, -17)).segment((-44, -17)).segment((-44, -23)).close().assemble().push([(54, 3)]).circle(2, mode='s').push([(-27, 12)]).parray(22, 346, 141, 2).face(cq.Workplane('XY').sketch().segment((-3, 1), (1, 3)).segment((3, -1)).segment((-1, -3)).close().assemble().wires(), mode='s').finalize()", -68)
r=extrude(r, (27, 25, -90), 'XY', "sketch().push([(27, 25)]).rect(24, 22).finalize()", -10)
r=extrude(r, (-12, -1, -22), 'XY', "sketch().push([(-12, -1)]).rect(36, 68).finalize()", 122)
