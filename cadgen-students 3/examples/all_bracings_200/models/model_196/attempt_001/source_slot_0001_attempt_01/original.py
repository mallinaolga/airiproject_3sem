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
r=extrude(r, (-96, 0, 0), 'YZ', "sketch().push([(-7, -1)]).circle(19).finalize()", 192)
r=extrude(r, (-33, -7, -1), 'YZ', "sketch().push([(-7, -1)]).circle(26).finalize()", 38, False)
r=extrude(r, (-76, -7, 18), 'XY', "sketch().push([(-76, -7)]).circle(4).finalize()", 14)
r=extrude(r, (-82, 12, -1), 'YZ', "sketch().arc((6, -14), (12, -1), (6, 12)).segment((19, 8)).arc((28, 12), (38, 8)).arc((42, -1), (38, -10)).arc((28, -14), (19, -10)).close().assemble().finalize()", 10)
r=extrude(r, (-3, 19, -1), 'ZX', "sketch().push([(-1, -3)]).circle(20).finalize()", 19)
r=extrude(r, (62, -7, -20), 'XY', "sketch().push([(62, -7)]).rect(14, 68).finalize()", -21)
r=extrude(r, (-27, -7, 25), 'XY', "sketch().segment((-48, -1), (-42, 9)).segment((-6, -13)).segment((-12, -23)).arc((-26, -6), (-48, -1)).assemble().finalize()", 15)
