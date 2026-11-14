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
r=extrude(r, (-17, 0, 0), 'YZ', "sketch().push([(-3, 1)]).circle(9).finalize()", -51)
r=extrude(r, (-63, -3, 1), 'YZ', "sketch().push([(-3, 1)]).circle(11).finalize()", -7, False)
r=extrude(r, (-42, 5, 1), 'ZX', "sketch().push([(1, -42)]).circle(51).finalize()", 4)
r=extrude(r, (10, 8, 1), 'ZX', "sketch().segment((-20, 4), (-20, 85)).segment((22, 85)).segment((22, 4)).arc((1, 10), (-20, 4)).assemble().finalize()", 4)
r=extrude(r, (31, 10, -20), 'XY', "sketch().push([(31, 10)]).circle(5).finalize()", -14)
r=extrude(r, (-26, -3, 10), 'YZ', "sketch().segment((-10, 5), (-8, 15)).arc((-10, 20), (-8, 26)).arc((-3, 28), (2, 26)).arc((4, 20), (2, 15)).segment((4, 5)).arc((-3, 10), (-10, 5)).assemble().finalize()", 119)
r=extrude(r, (26, 10, -29), 'XY', "sketch().arc((17, 7), (16, 10), (17, 13)).arc((20, 14), (23, 13)).segment((29, 14)).arc((26, 10), (29, 6)).segment((23, 7)).arc((20, 6), (17, 7)).assemble().finalize()", -23)
