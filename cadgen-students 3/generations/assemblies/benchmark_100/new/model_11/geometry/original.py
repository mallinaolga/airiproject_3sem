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
r=extrude(r, (-110, 0, 0), 'YZ', "sketch().push([(0.5, -2.5)]).rect(49, 61).finalize()", 219)
r=extrude(r, (-4, 0, -3), 'YZ', "sketch().push([(0, -3)]).rect(80, 100).finalize()", 55, False)
r=extrude(r, (62, 23, -1), 'ZX', "sketch().push([(-1, 62)]).circle(13).finalize()", 26)
r=extrude(r, (103, 6, 25), 'XY', "sketch().segment((97, 3), (97, 6)).segment((109, 9)).segment((109, 6)).close().assemble().finalize()", 49)
r=extrude(r, (26, -40, 34), 'ZX', "sketch().push([(34, 26)]).circle(5).finalize()", -9)
r=extrude(r, (-56, 23, -28), 'ZX', "sketch().push([(-28, -56)]).circle(46).finalize()", 25)
