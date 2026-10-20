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
r=extrude(r, (0, 0, -87), 'XY', "sketch().segment((-32, -72), (-32, 68)).segment((100, 68)).segment((100, 4)).arc((71, -29), (64, -72)).close().assemble().push([(26, 44)]).circle(10, mode='s').push([(10, -41)]).parray(28, 302, 111, 9).face(cq.Workplane('XY').sketch().segment((-2, 0), (-2, 1)).segment((-1, 1)).arc((0, 1), (1, 0)).segment((2, 0)).segment((2, -1)).segment((1, -1)).arc((0, -1), (-1, 0)).close().assemble().wires(), mode='s').finalize()", 61)
r=extrude(r, (-24, 0, -26), 'XY', "sketch().push([(-24, 0)]).circle(76).finalize()", 114)
