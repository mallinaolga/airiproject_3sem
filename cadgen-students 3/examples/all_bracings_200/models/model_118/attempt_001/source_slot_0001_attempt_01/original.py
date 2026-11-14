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
r=extrude(r, (0, 0, 79), 'XY', "sketch().push([(-3, 0)]).circle(13).finalize()", -170)
r=extrude(r, (-3, 0, -12), 'XY', "sketch().push([(-3, 0)]).circle(18).finalize()", -19, False)
r=extrude(r, (10, 0, -68), 'YZ', "sketch().push([(0, -68)]).circle(12).push([(0, -68)]).circle(6, mode='s').finalize()", 8)
r=extrude(r, (7, 3, 79), 'ZX', "sketch().push([(84, 7)]).rect(10, 28).finalize()", -3)
r=extrude(r, (10, 0, 33), 'YZ', "sketch().push([(0, 33)]).rect(12, 4).finalize()", 3)
