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
r=extrude(r, (-85, 0, 0), 'YZ', "sketch().push([(3, 0)]).circle(18).finalize()", 186)
r=extrude(r, (-56, 3, 0), 'YZ', "sketch().push([(3, 0)]).circle(31).finalize()", 24, False)
r=extrude(r, (-81, 3, 17), 'XY', "sketch().push([(-81, 3)]).rect(34, 30).finalize()", 14)
r=extrude(r, (9, 21, 0), 'ZX', "sketch().push([(0, 9)]).rect(10, 36).finalize()", 8)
r=extrude(r, (-81, -16, 0), 'YZ', "sketch().arc((-29, -4), (-31, 0), (-29, 4)).arc((-25, 6), (-21, 4)).segment((-15, 6)).arc((-16, 0), (-15, -6)).segment((-21, -4)).arc((-25, -6), (-29, -4)).assemble().finalize()", -19)
r=extrude(r, (-48, -29, 0), 'ZX', "sketch().push([(0, -48)]).rect(4, 2).finalize()", -6)
