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
r=extrude(r, (105, 0, 0), 'YZ', "sketch().push([(0, -1)]).rect(40, 20).finalize()", -210)
r=extrude(r, (68, 0, -1), 'YZ', "sketch().push([(0, -1)]).rect(48, 26).finalize()", -57, False)
r=extrude(r, (68, -19, -10), 'YZ', "sketch().push([(-19, -10)]).rect(10, 2).finalize()", 34)
r=extrude(r, (26, 21, 12), 'XY', "sketch().push([(26, 21)]).circle(2).finalize()", 1)
