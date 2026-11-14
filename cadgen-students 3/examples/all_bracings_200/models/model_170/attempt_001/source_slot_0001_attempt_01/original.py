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
r=extrude(r, (0, 0, 118), 'XY', "sketch().push([(-26, 37)]).circle(19).finalize()", -235)
r=extrude(r, (-26, 37, -11), 'XY', "sketch().push([(-26, 37)]).circle(23).finalize()", -47, False)
r=extrude(r, (-7, 37, -67), 'YZ', "sketch().push([(37, -67)]).circle(3).finalize()", 35)
r=extrude(r, (-26, 18, -84), 'XY', "sketch().segment((-32, -59), (-32, 20)).arc((-26, 18), (-20, 20)).segment((-20, -59)).close().assemble().finalize()", 13)
r=extrude(r, (12, 34, -67), 'YZ', "sketch().segment((-22, -69), (-22, -65)).segment((35, -65)).arc((34, -67), (35, -69)).close().assemble().finalize()", 37)
