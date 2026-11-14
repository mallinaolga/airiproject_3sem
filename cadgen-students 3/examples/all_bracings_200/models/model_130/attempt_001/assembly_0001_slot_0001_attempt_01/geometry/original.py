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
r=extrude(r, (0, 0, 94), 'XY', "sketch().push([(6, 11)]).circle(29).finalize()", -132)
r=extrude(r, (6, 11, 11), 'XY', "sketch().push([(6, 11)]).circle(45).finalize()", -49, False)
r=extrude(r, (6, -34, -17), 'ZX', "sketch().segment((-19, 6), (-16, 7)).segment((-15, 6)).segment((-18, 5)).close().assemble().finalize()", -15)
r=extrude(r, (50, 11, -37), 'YZ', "sketch().push([(11, -37)]).circle(73).finalize()", 27)
r=extrude(r, (12, -9, 94), 'XY', "sketch().push([(12, -9)]).circle(50).finalize()", 15)
r=extrude(r, (50, -60, -24), 'YZ', "sketch().push([(-60, -24)]).rect(46, 30).finalize()", -52)
r=extrude(r, (-39, 11, -25), 'XY', "sketch().segment((-78, -2), (-78, 24)).segment((-36, 24)).arc((-39, 11), (-36, -2)).close().assemble().finalize()", 64)
