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
r=extrude(r, (-117, 0, 0), 'YZ', "sketch().push([(-49, 4)]).circle(21).finalize()", 234)
r=extrude(r, (3, -49, 4), 'YZ', "sketch().push([(-49, 4)]).circle(30).finalize()", 64, False)
r=extrude(r, (21, -49, -26), 'XY', "sketch().push([(21, -49)]).rect(22, 28).finalize()", -9)
r=extrude(r, (-17, -28, 4), 'ZX', "sketch().push([(4, -17)]).circle(2).finalize()", 108)
