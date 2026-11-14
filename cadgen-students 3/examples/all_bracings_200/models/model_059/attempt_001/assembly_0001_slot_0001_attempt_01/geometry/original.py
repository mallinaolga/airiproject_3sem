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
r=extrude(r, (0, -102, 0), 'ZX', "sketch().push([(14, -21)]).rect(52, 20).finalize()", 220)
r=extrude(r, (-21, 84, 14), 'ZX', "sketch().push([(14, -21)]).rect(82, 30).finalize()", 28, False)
r=extrude(r, (-30, -82, -12), 'YZ', "sketch().segment((-118, -12), (-107, 9)).arc((-118, 34), (-107, 59)).arc((-82, 69), (-57, 59)).arc((-46, 34), (-57, 9)).segment((-46, -12)).close().assemble().finalize()", 42)
r=extrude(r, (12, -111, 36), 'YZ', "sketch().arc((-109, 33), (-113, 39), (-108, 34)).arc((-108, 32), (-109, 33)).assemble().finalize()", 24)
r=extrude(r, (-11, -27, 0), 'YZ', "sketch().push([(-27, 0)]).rect(46, 32).finalize()", 45)
r=extrude(r, (-21, -6, -12), 'XY', "sketch().push([(-21, -6)]).circle(2).finalize()", -57)
