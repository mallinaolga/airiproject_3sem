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
r=extrude(r, (0, 93, 0), 'ZX', "sketch().push([(-11.5, -5)]).rect(33, 24).finalize()", -186)
r=extrude(r, (-5, 32, -12), 'ZX', "sketch().push([(-12, -5)]).rect(40, 30).finalize()", -58, False)
r=extrude(r, (7, 92, -15), 'YZ', "sketch().push([(92, -15)]).circle(4).push([(91, -14)]).circle(1, mode='s').finalize()", 2)
r=extrude(r, (1, -38, -28), 'XY', "sketch().push([(1, -38)]).rect(6, 4).finalize()", -31)
r=extrude(r, (10, -20, 0), 'YZ', "sketch().push([(-20, 0)]).circle(76).finalize()", 11)
