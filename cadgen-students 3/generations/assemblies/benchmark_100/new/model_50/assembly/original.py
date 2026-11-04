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
r=extrude(r, (0, 0, 97), 'XY', "sketch().push([(19, 10)]).circle(44).finalize()", -214)
r=extrude(r, (19, 10, 4), 'XY', "sketch().push([(19, 10)]).circle(76).finalize()", -85, False)
r=extrude(r, (19, -34, 71), 'XY', "sketch().segment((-10, -105), (-10, -22)).arc((19, -34), (48, -22)).segment((48, -105)).close().assemble().finalize()", 47)
r=extrude(r, (38, -53, 4), 'ZX', "sketch().segment((4, -4), (4, 80)).segment((16, 54)).arc((32, 61), (49, 54)).arc((56, 38), (49, 22)).arc((32, 15), (16, 22)).close().assemble().finalize()", -42)
r=extrude(r, (27, 47, 97), 'XY', "sketch().segment((36, -4), (38, -12)).arc((8, 103), (54, -6)).segment((53, 0)).close().assemble().finalize()", 4)
r=extrude(r, (-9, -71, 113), 'YZ', "sketch().push([(-71, 113)]).circle(4).finalize()", -33)
r=extrude(r, (-9, -82, 97), 'YZ', "sketch().segment((-88, 96), (-88, 98)).segment((-86, 98)).segment((-86, 99)).segment((-78, 99)).segment((-78, 98)).segment((-76, 98)).segment((-76, 96)).segment((-78, 96)).segment((-78, 95)).segment((-86, 95)).segment((-86, 96)).close().assemble().finalize()", -86)
