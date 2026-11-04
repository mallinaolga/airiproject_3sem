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
r=extrude(r, (0, 0, -109), 'XY', "sketch().push([(-11.5, 0)]).rect(3, 26).finalize()", 218)
r=extrude(r, (-11, 0, -64), 'XY', "sketch().push([(-11, 0)]).rect(4, 36).finalize()", 35, False)
r=extrude(r, (-9, 5, 90), 'YZ', "sketch().push([(5, 90)]).rect(6, 18).finalize()", 16)
r=extrude(r, (-9, 0, -76), 'YZ', "sketch().push([(0, -76)]).circle(3).finalize()", 33)
r=extrude(r, (-12, -10, -88), 'YZ', "sketch().push([(-10, -88)]).circle(1).finalize()", -5)
r=extrude(r, (-9, 12, -57), 'ZX', "sketch().segment((-66, -9), (-63, -5)).arc((-65, 1), (-63, 7)).arc((-57, 9), (-51, 7)).arc((-49, 1), (-51, -5)).segment((-48, -9)).close().assemble().finalize()", -1)
r=extrude(r, (-12, -2, 18), 'YZ', "sketch().segment((-17, 21), (0, 33)).segment((13, 15)).segment((-4, 3)).close().assemble().finalize()", -11)
r=extrude(r, (-9, 5, 27), 'YZ', "sketch().segment((0, 37), (5, 38)).segment((10, 17)).segment((5, 16)).close().assemble().finalize()", 9)
