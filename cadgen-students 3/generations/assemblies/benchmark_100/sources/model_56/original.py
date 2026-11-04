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
r=extrude(r, (0, 0, -116), 'XY', "sketch().push([(1, 0)]).rect(20, 36).finalize()", 232)
r=extrude(r, (1, 0, -45), 'XY', "sketch().push([(1, 0)]).rect(28, 52).finalize()", 30, False)
r=extrude(r, (-10, 12, -59), 'YZ', "sketch().push([(12, -59)]).rect(18, 8).finalize()", -1)
r=extrude(r, (-10, -7, -95), 'YZ', "sketch().push([(-7, -95)]).circle(4).finalize()", -2)
r=extrude(r, (-11, -7, -91), 'XY', "sketch().push([(-11, -7)]).rect(8, 8).finalize()", 3)
