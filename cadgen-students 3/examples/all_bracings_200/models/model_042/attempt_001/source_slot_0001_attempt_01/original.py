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
r=extrude(r, (75, 0, 0), 'YZ', "sketch().push([(-1, -3)]).rect(8, 28).finalize()", -172)
r=extrude(r, (71, -1, -4), 'YZ', "sketch().push([(-1, -4)]).rect(14, 44).finalize()", -66, False)
r=extrude(r, (67, -7, -18), 'ZX', "sketch().push([(-18, 67)]).circle(2).finalize()", -3)
r=extrude(r, (64, -4, -26), 'XY', "sketch().segment((50, -3), (66, 8)).segment((78, -9)).segment((67, -16)).segment((67, -3)).close().assemble().finalize()", -2)
r=extrude(r, (43, -7, 8), 'ZX', "sketch().segment((-12, 54), (18, 64)).segment((28, 32)).segment((-2, 22)).close().assemble().finalize()", -9)
r=extrude(r, (75, 1, 9), 'XY', "sketch().push([(86, 1)]).rect(22, 34).finalize()", -7)
r=extrude(r, (58, -16, 13), 'ZX', "sketch().push([(13, 58)]).circle(7).finalize()", -1)
