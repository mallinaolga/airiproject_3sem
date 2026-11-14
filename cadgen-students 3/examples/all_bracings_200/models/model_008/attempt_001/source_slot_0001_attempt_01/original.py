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
r=extrude(r, (0, -57, 0), 'ZX', "sketch().push([(42, 47)]).circle(31).finalize()", 104)
r=extrude(r, (47, -53, 42), 'ZX', "sketch().push([(42, 47)]).circle(47).finalize()", 27, False)
r=extrude(r, (45, 48, 12), 'ZX', "sketch().push([(12, 45)]).circle(1).finalize()", 29)
r=extrude(r, (47, 16, 11), 'XY', "sketch().segment((45, 16), (46, 17)).segment((49, 17)).segment((48, 15)).close().assemble().finalize()", -95)
r=extrude(r, (47, -34, -5), 'XY', "sketch().push([(47, -34)]).circle(29).finalize()", -87)
r=extrude(r, (1, -40, 42), 'YZ', "sketch().push([(-40, 42)]).circle(37).finalize()", -94)
r=extrude(r, (47, -63, -7), 'XY', "sketch().segment((34, -65), (34, -58)).arc((47, -63), (60, -58)).segment((60, -65)).close().assemble().finalize()", 61)
r=extrude(r, (-8, -3, 42), 'ZX', "sketch().segment((33, -14), (34, 0)).segment((51, -2)).segment((50, -16)).close().assemble().finalize()", 2)
r=extrude(r, (-5, -40, 78), 'XY', "sketch().push([(-5, -40)]).circle(1).finalize()", 14)
