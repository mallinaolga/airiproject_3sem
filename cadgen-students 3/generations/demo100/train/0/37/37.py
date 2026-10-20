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
r=extrude(r, (-100, 0, 0), 'YZ', "sketch().push([(58.5, 0)]).rect(21, 34).finalize()", 200)
r=extrude(r, (-59, 48, 0), 'ZX', "sketch().segment((-12, -96), (-12, -22)).segment((1, -22)).segment((1, -52)).arc((12, -64), (1, -75)).segment((1, -96)).close().assemble().reset().face(cq.Workplane('ZX').sketch().arc((-10, -61), (-9, -56), (-5, -54)).arc((-8, -57), (-10, -61)).assemble(), mode='s').finalize()", -117)
