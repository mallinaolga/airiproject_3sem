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
r=extrude(r, (-81, 0, 0), 'YZ', "sketch().push([(0, 5)]).rect(32, 22).finalize()", 175)
r=extrude(r, (-4, 0, 5), 'YZ', "sketch().push([(0, 5)]).rect(52, 36).finalize()", 84, False)
r=extrude(r, (-64, -16, -6), 'YZ', "sketch().push([(-13.5, -6)]).rect(5, 46).finalize()", -30)
r=extrude(r, (87, 16, -3), 'ZX', "sketch().push([(-3, 87)]).circle(1).finalize()", 11)
r=extrude(r, (-69, -16, 1), 'ZX', "sketch().push([(1, -69)]).rect(56, 12).finalize()", -10)
