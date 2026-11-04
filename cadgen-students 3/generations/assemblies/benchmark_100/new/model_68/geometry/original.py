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
r=extrude(r, (0, 79, 0), 'ZX', "sketch().push([(-4, 0)]).circle(10).finalize()", -178)
r=extrude(r, (0, 50, -4), 'ZX', "sketch().push([(-4, 0)]).circle(14).finalize()", -36, False)
r=extrude(r, (0, -95, 6), 'XY', "sketch().push([(0, -95)]).rect(50, 22).finalize()", 45)
r=extrude(r, (-3, 79, -2), 'YZ', "sketch().segment((79, -51), (79, 47)).segment((85, 6)).arc((94, 10), (102, 6)).arc((106, -2), (102, -10)).arc((94, -14), (85, -10)).close().assemble().finalize()", -17)
