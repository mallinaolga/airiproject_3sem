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
r=extrude(r, (-104, 0, 0), 'YZ', "sketch().push([(-0.5, -9)]).rect(35, 18).finalize()", 209)
r=extrude(r, (-67, 0, -9), 'YZ', "sketch().push([(0, -9)]).rect(56, 28).finalize()", 57, False)
r=extrude(r, (94, -18, -4), 'ZX', "sketch().push([(-4, 94)]).circle(3).finalize()", -16)
r=extrude(r, (-88, -18, -5), 'YZ', "sketch().push([(8.5, -5)]).rect(53, 6).finalize()", 3)
r=extrude(r, (-19, 7, 5), 'XY', "sketch().push([(-19, 7)]).rect(2, 16).finalize()", 18)
r=extrude(r, (-68, -9, -21), 'YZ', "sketch().push([(-9, -21)]).circle(1).finalize()", -7)
r=extrude(r, (-92, 17, -16), 'ZX', "sketch().push([(-16, -92)]).circle(1).finalize()", 5)
