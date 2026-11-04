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
r=extrude(r, (0, 0, 52), 'XY', "sketch().push([(-15, -6)]).circle(24).finalize()", -86)
r=extrude(r, (-15, -6, -24), 'XY', "sketch().push([(-15, -6)]).circle(33).finalize()", -14, False)
r=extrude(r, (-31, -19, 52), 'XY', "sketch().push([(-31, -19)]).circle(51).finalize()", 32)
r=extrude(r, (20, -19, 53), 'XY', "sketch().arc((-3, -61), (20, -19), (-3, 23)).segment((96, 23)).segment((96, -61)).close().assemble().finalize()", -70)
r=extrude(r, (-29, 4, -39), 'XY', "sketch().segment((-67, -10), (30, -44)).arc((-97, 38), (45, -15)).segment((-56, 21)).close().assemble().finalize()", -60)
r=extrude(r, (-29, -72, -76), 'ZX', "sketch().push([(-76, -29)]).circle(33).finalize()", -8)
r=extrude(r, (23, -52, 53), 'XY', "sketch().push([(23, -52)]).circle(4).finalize()", 56)
r=extrude(r, (81, 22, 29), 'ZX', "sketch().segment((4, 87), (38, 105)).segment((54, 75)).segment((20, 57)).close().assemble().finalize()", 39)
