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
r=extrude(r, (0, -63, 0), 'ZX', "sketch().push([(0, 5)]).rect(86, 24).finalize()", 170)
r=extrude(r, (5, -24, 0), 'ZX', "sketch().push([(0, 5)]).rect(124, 36).finalize()", 19, False)
r=extrude(r, (5, -24, -44), 'ZX', "sketch().push([(-44, 5)]).circle(5).finalize()", -82)
r=extrude(r, (-13, -14, -53), 'YZ', "sketch().push([(-14, -53)]).rect(82, 18).finalize()", -12)
r=extrude(r, (17, 12, -34), 'YZ', "sketch().push([(12, -34)]).circle(5).finalize()", 8)
