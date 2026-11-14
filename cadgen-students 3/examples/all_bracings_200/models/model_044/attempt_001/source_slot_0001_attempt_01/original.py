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
r=extrude(r, (0, 0, 88), 'XY', "sketch().push([(10, 4)]).circle(15).finalize()", -187)
r=extrude(r, (10, 4, -66), 'XY', "sketch().push([(10, 4)]).circle(21).finalize()", -20, False)
r=extrude(r, (6, -4, 88), 'XY', "sketch().push([(6, -4)]).circle(1).finalize()", 11)
r=extrude(r, (-5, 4, -35), 'YZ', "sketch().push([(4, -35)]).circle(24).finalize()", -26)
r=extrude(r, (10, -11, 8), 'XY', "sketch().segment((-1, -28), (-1, -5)).arc((10, -11), (21, -5)).segment((21, -28)).close().assemble().finalize()", 31)
