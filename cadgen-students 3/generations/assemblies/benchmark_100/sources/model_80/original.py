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
r=extrude(r, (65, 0, 0), 'YZ', "sketch().push([(6, -5)]).circle(7).finalize()", -100)
r=extrude(r, (-34, 6, -5), 'YZ', "sketch().push([(6, -5)]).circle(10).finalize()", -29, False)
r=extrude(r, (-33, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(119).finalize()", 112)
r=extrude(r, (-63, 5, -6), 'YZ', "sketch().push([(5, -6)]).circle(4).finalize()", -20)
r=extrude(r, (-34, 70, 72), 'YZ', "sketch().push([(70, 72)]).circle(45).finalize()", -58)
r=extrude(r, (79, -25, -10), 'YZ', "sketch().push([(-25, -10)]).rect(76, 198).finalize()", 13)
