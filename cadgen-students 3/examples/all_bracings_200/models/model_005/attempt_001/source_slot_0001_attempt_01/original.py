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
r=extrude(r, (0, 0, -104), 'XY', "sketch().push([(0, 3)]).rect(12, 30).finalize()", 197)
r=extrude(r, (0, 3, 75), 'XY', "sketch().push([(0, 3)]).rect(16, 40).finalize()", 29, False)
r=extrude(r, (8, -10, 89), 'YZ', "sketch().push([(-10, 89)]).circle(5).finalize()", 9)
r=extrude(r, (-4, -12, -12), 'ZX', "sketch().push([(-12, -4)]).rect(12, 24).finalize()", -15)
r=extrude(r, (-6, 11, 5), 'YZ', "sketch().push([(11, 5)]).circle(16).finalize()", -7)
