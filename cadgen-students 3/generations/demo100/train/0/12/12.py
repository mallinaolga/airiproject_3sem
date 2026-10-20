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
r=extrude(r, (0, 0, 1), 'XY', "sketch().push([(7, 4)]).rect(124, 54).push([(0, 0)]).circle(17, mode='s').push([(-45, 7)]).circle(4, mode='s').push([(-10, 14)]).parray(9, 298, 354, 12).circle(1, mode='s').finalize()", -4)
r=extrude(r, (-36, -25, 0), 'ZX', "sketch().push([(0, -36)]).rect(200, 70).finalize()", -5)
