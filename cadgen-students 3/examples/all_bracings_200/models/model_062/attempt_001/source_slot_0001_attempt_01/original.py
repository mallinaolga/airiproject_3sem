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
r=extrude(r, (0, -67, 0), 'ZX', "sketch().push([(7.5, 51)]).rect(71, 2).finalize()", 163)
r=extrude(r, (51, -31, 8), 'ZX', "sketch().push([(8, 51)]).rect(84, 2).finalize()", 27, False)
r=extrude(r, (52, 28, 33), 'XY', "sketch().push([(0.5, 28)]).rect(103, 6).finalize()", 16)
r=extrude(r, (50, -47, 0), 'YZ', "sketch().push([(-47, 0)]).circle(50).finalize()", -34)
r=extrude(r, (15, -93, 11), 'YZ', "sketch().push([(-93, 11)]).circle(1).finalize()", -35)
r=extrude(r, (15, -20, -18), 'YZ', "sketch().push([(-20, -18)]).rect(24, 8).finalize()", -14)
