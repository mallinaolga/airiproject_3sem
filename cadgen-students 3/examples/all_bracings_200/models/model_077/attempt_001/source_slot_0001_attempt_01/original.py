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
r=extrude(r, (0, 0, -99), 'XY', "sketch().push([(-15, -13.5)]).rect(2, 19).finalize()", 160)
r=extrude(r, (-15, -13, 57), 'XY', "sketch().push([(-15, -13)]).rect(4, 34).finalize()", 41, False)
r=extrude(r, (-14, -11, 6), 'YZ', "sketch().segment((-13, 5), (-13, 6)).segment((-13, 7)).segment((-11, 8)).segment((-10, 7)).segment((-9, 7)).segment((-9, 6)).segment((-9, 5)).segment((-11, 4)).segment((-12, 5)).close().assemble().finalize()", 2)
r=extrude(r, (-13, -9, 6), 'YZ', "sketch().segment((-9, -12), (-9, 24)).segment((0, 19)).arc((13, 24), (25, 19)).arc((30, 6), (25, -7)).arc((13, -12), (0, -7)).close().assemble().finalize()", 24)
r=extrude(r, (-15, -4, -5), 'ZX', "sketch().push([(-5, -15)]).circle(2).finalize()", 28)
r=extrude(r, (0, 13, -13), 'XY', "sketch().push([(0, 13)]).rect(40, 20).finalize()", -44)
