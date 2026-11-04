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
r=extrude(r, (0, 0, -55), 'XY', "sketch().push([(-7.5, 60.5)]).rect(37, 1).finalize()", 157)
r=extrude(r, (-7, 60, -36), 'XY', "sketch().push([(-7, 60)]).rect(46, 2).finalize()", 20, False)
r=extrude(r, (-27, 53, 1), 'ZX', "sketch().push([(1, -27)]).rect(40, 66).finalize()", -69)
r=extrude(r, (-15, 61, -21), 'XY', "sketch().segment((-54, 61), (24, 61)).segment((12, 32)).arc((24, 5), (12, -22)).arc((-15, -34), (-42, -22)).arc((-54, 5), (-42, 32)).close().assemble().finalize()", -70)
r=extrude(r, (24, 5, -40), 'XY', "sketch().arc((13, -20), (24, 5), (13, 30)).segment((98, 30)).segment((98, -20)).close().assemble().finalize()", 22)
r=extrude(r, (83, 30, -34), 'ZX', "sketch().push([(-34, 83)]).circle(1).finalize()", 50)
r=extrude(r, (-15, -34, -28), 'ZX', "sketch().push([(-28, -15)]).circle(73).finalize()", -22)
r=extrude(r, (-30, -56, -29), 'ZX', "sketch().segment((-103, -3), (12, 37)).segment((45, -57)).segment((-70, -97)).close().assemble().finalize()", -25)
