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
r=extrude(r, (0, -106, 0), 'ZX', "sketch().push([(2.5, 2)]).rect(35, 16).finalize()", 125)
r=extrude(r, (2, -48, 2), 'ZX', "sketch().push([(2, 2)]).rect(40, 18).finalize()", 42, False)
r=extrude(r, (-1, 8, 20), 'YZ', "sketch().segment((-90, 20), (106, 20)).segment((20, 11)).arc((25, -1), (20, -13)).arc((8, -18), (-4, -13)).arc((-9, -1), (-4, 11)).close().assemble().push([(8, -16)]).circle(1, mode='s').finalize()", 10)
r=extrude(r, (11, -20, 8), 'YZ', "sketch().arc((-25, 3), (-26, 11), (-20, 15)).segment((-19, 15)).segment((-18, 15)).arc((-17, 14), (-16, 14)).segment((-15, 13)).arc((-14, 5), (-20, 1)).segment((-21, 1)).segment((-22, 1)).arc((-23, 2), (-24, 2)).close().assemble().finalize()", 6)
r=extrude(r, (-6, -87, -13), 'YZ', "sketch().segment((-93, -21), (-85, -4)).segment((-81, -5)).segment((-89, -22)).close().assemble().finalize()", -10)
r=extrude(r, (-6, -57, -3), 'YZ', "sketch().push([(-57, -3)]).circle(2).finalize()", -11)
