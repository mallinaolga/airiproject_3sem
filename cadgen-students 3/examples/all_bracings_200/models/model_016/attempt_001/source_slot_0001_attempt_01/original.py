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
r=extrude(r, (0, 0, -113), 'XY', "sketch().push([(-4.5, -3.5)]).rect(9, 35).finalize()", 227)
r=extrude(r, (-5, -4, 60), 'XY', "sketch().push([(-5, -4)]).rect(14, 54).finalize()", 23, False)
r=extrude(r, (1, 15, 105), 'YZ', "sketch().push([(15, 105)]).circle(8).finalize()", 18)
r=extrude(r, (-11, 15, 63), 'YZ', "sketch().push([(15, 63)]).circle(16).finalize()", -8)
