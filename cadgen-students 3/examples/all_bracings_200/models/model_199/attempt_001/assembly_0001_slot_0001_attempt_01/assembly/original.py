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
r=extrude(r, (0, 0, 14), 'XY', "sketch().push([(-3, 63)]).circle(10).finalize()", -75)
r=extrude(r, (-3, 63, -14), 'XY', "sketch().push([(-3, 63)]).circle(16).finalize()", -14, False)
r=extrude(r, (-10, 59, -60), 'XY', "sketch().push([(-10, 59)]).rect(2, 2).finalize()", -50)
r=extrude(r, (-5, 54, 14), 'ZX', "sketch().push([(61.5, -5)]).rect(95, 210).finalize()", -64)
r=extrude(r, (54, -10, 47), 'ZX', "sketch().push([(47, 54)]).circle(57).finalize()", -45)
r=extrude(r, (48, -54, 56), 'ZX', "sketch().push([(56, 48)]).circle(24).finalize()", -25)
