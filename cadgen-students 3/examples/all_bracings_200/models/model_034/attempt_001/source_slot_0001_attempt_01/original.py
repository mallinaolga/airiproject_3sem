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
r=extrude(r, (0, 0, -104), 'XY', "sketch().push([(-1.5, 6.5)]).rect(3, 73).finalize()", 207)
r=extrude(r, (-1, 6, -24), 'XY', "sketch().push([(-1, 6)]).rect(4, 96).finalize()", 63, False)
r=extrude(r, (-3, -29, 68), 'YZ', "sketch().arc((-56, 55), (-6, 87), (-47, 44)).arc((-44, 56), (-56, 55)).assemble().finalize()", -60)
r=extrude(r, (-2, 43, -61), 'ZX', "sketch().push([(-61, -2)]).rect(2, 2).finalize()", 11)
r=extrude(r, (1, -9, 12), 'YZ', "sketch().push([(-9, 12)]).circle(41).finalize()", 51)
r=extrude(r, (52, -1, -11), 'YZ', "sketch().segment((-6, -13), (-6, -5)).segment((4, -5)).segment((4, -13)).segment((0, -13)).segment((0, -17)).segment((-5, -17)).segment((-5, -13)).close().assemble().finalize()", 11)
r=extrude(r, (-3, 37, 77), 'YZ', "sketch().push([(37, 77)]).circle(22).finalize()", -17)
