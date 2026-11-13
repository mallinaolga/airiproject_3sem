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
r=extrude(r, (0, 0, 92), 'XY', "sketch().push([(0, 0)]).circle(27).finalize()", -163)
r=extrude(r, (0, 0, -58), 'XY', "sketch().push([(0, 0)]).circle(43).finalize()", -42, False)
r=extrude(r, (33, 21, -58), 'XY', "sketch().segment((30, 15), (30, 16)).arc((32, 27), (37, 17)).segment((37, 15)).close().assemble().finalize()", 113)
r=extrude(r, (36, 18, 55), 'XY', "sketch().segment((34, 17), (36, 20)).segment((38, 19)).segment((36, 16)).close().assemble().finalize()", 45)
