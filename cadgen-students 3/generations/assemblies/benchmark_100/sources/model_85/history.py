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
r=extrude(r, (0, 0, -116), 'XY', "sketch().push([(0, -1)]).rect(30, 2).finalize()", 224)
r=extrude(r, (0, -1, -56), 'XY', "sketch().push([(0, -1)]).rect(46, 4).finalize()", 49, False)
r=extrude(r, (-12, 0, 106), 'YZ', "sketch().arc((-15, 101), (-17, 106), (-15, 111)).arc((-9, 114), (-4, 111)).segment((0, 116)).segment((0, 96)).segment((-4, 101)).arc((-9, 98), (-15, 101)).assemble().finalize()", 17)
r=extrude(r, (-15, 0, 19), 'YZ', "sketch().push([(0, 19)]).circle(29).finalize()", -3)
r=extrude(r, (-15, 3, 33), 'YZ', "sketch().push([(3, 33)]).circle(1).finalize()", 13)
