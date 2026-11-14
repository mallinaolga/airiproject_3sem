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
r=extrude(r, (0, 18, 0), 'ZX', "sketch().push([(21, 3)]).circle(5).finalize()", 94)
r=extrude(r, (3, 49, 21), 'ZX', "sketch().push([(21, 3)]).circle(6).finalize()", 11, False)
r=extrude(r, (2, 49, 16), 'XY', "sketch().push([(2, -32.5)]).rect(188, 163).finalize()", -30)
r=extrude(r, (61, 39, 16), 'XY', "sketch().push([(61, 39)]).rect(18, 22).finalize()", 12)
r=extrude(r, (-40, -110, 0), 'ZX', "sketch().push([(0, -40)]).circle(57).finalize()", -2)
r=extrude(r, (3, 44, 26), 'XY', "sketch().push([(3, 44)]).circle(20).push([(3, 44)]).circle(15, mode='s').finalize()", 20)
r=extrude(r, (66, 28, 20), 'ZX', "sketch().arc((20, 68), (20, 65), (21, 67)).arc((19, 64), (20, 68)).assemble().finalize()", -31)
