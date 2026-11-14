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
r=extrude(r, (0, 0, -114), 'XY', "sketch().push([(-12, 35)]).circle(40).finalize()", 227)
r=extrude(r, (-12, 35, 1), 'XY', "sketch().push([(-12, 35)]).circle(46).finalize()", 66, False)
r=extrude(r, (35, 35, 25), 'YZ', "sketch().push([(35, 25)]).circle(58).finalize()", 25)
r=extrude(r, (-12, -5, -70), 'XY', "sketch().segment((-24, -93), (-24, -2)).arc((-12, -5), (0, -2)).segment((0, -93)).close().assemble().finalize()", 16)
r=extrude(r, (-24, -37, -65), 'YZ', "sketch().segment((-46, -72), (-34, -57)).segment((-30, -61)).segment((-30, -52)).segment((-29, -52)).segment((-29, -62)).segment((-28, -63)).segment((-29, -64)).segment((-29, -67)).segment((-30, -67)).segment((-30, -66)).segment((-40, -78)).close().assemble().finalize()", -36)
r=extrude(r, (-12, 74, -66), 'ZX', "sketch().push([(-66, -12)]).rect(30, 12).finalize()", 15)
