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
r=extrude(r, (0, 103, 0), 'ZX', "sketch().push([(5, -0.5)]).rect(30, 29).finalize()", -208)
r=extrude(r, (-1, -40, 5), 'ZX', "sketch().push([(5, -1)]).rect(42, 42).finalize()", -21, False)
r=extrude(r, (-1, 103, -8), 'ZX', "sketch().push([(-8, -1)]).circle(1).finalize()", 2)
r=extrude(r, (5, -96, -10), 'XY', "sketch().push([(5, -96)]).rect(12, 8).finalize()", -16)
r=extrude(r, (9, -83, -10), 'XY', "sketch().push([(9, -83)]).rect(6, 2).finalize()", -5)
r=extrude(r, (14, -91, -1), 'YZ', "sketch().push([(-91, -1)]).circle(4).finalize()", 8)
