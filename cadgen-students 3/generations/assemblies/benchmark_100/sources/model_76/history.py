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
r=extrude(r, (0, 0, -120), 'XY', "sketch().push([(3, 9)]).rect(16, 24).finalize()", 240)
r=extrude(r, (3, 9, 82), 'XY', "sketch().push([(3, 9)]).rect(24, 38).finalize()", 26, False)
r=extrude(r, (0, -3, -60), 'ZX', "sketch().push([(-60, 0)]).circle(23).finalize()", -25)
r=extrude(r, (21, -3, -54), 'ZX', "sketch().push([(-54, 21)]).circle(1).finalize()", 5)
