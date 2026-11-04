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
r=extrude(r, (94, 0, 0), 'YZ', "sketch().push([(-10.5, -2)]).rect(19, 10).finalize()", -188)
r=extrude(r, (-42, -10, -2), 'YZ', "sketch().push([(-10, -2)]).rect(32, 16).finalize()", -20, False)
r=extrude(r, (-89, -12, 3), 'XY', "sketch().push([(-89, -12)]).circle(3).finalize()", 13)
r=extrude(r, (89, -1, -2), 'ZX', "sketch().push([(-2, 89)]).circle(1).finalize()", 27)
r=extrude(r, (-35, -6, -7), 'XY', "sketch().push([(-35, -6)]).rect(2, 6).finalize()", -9)
