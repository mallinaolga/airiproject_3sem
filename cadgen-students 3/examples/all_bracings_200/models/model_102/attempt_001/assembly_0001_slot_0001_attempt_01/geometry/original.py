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
r=extrude(r, (0, 102, 0), 'ZX', "sketch().push([(2.5, -1.5)]).rect(27, 7).finalize()", -212)
r=extrude(r, (-2, 94, 2), 'ZX', "sketch().push([(2, -2)]).rect(48, 12).finalize()", -36, False)
r=extrude(r, (-3, 92, -21), 'YZ', "sketch().push([(92, -17.5)]).rect(36, 7).finalize()", -1)
r=extrude(r, (-4, 82, -21), 'XY', "sketch().push([(-4, 82)]).rect(6, 22).finalize()", -5)
r=extrude(r, (2, 98, -7), 'ZX', "sketch().segment((-18, 2), (-18, 5)).segment((-18, 9)).segment((4, 4)).segment((4, 2)).close().assemble().finalize()", 2)
r=extrude(r, (-1, 102, -2), 'ZX', "sketch().push([(-2, -1)]).circle(7).finalize()", 6)
r=extrude(r, (-8, 76, -10), 'YZ', "sketch().push([(76, -10)]).circle(5).finalize()", -1)
