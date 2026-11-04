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
r=extrude(r, (88, 0, 0), 'YZ', "sketch().push([(4, -10)]).circle(10).finalize()", -187)
r=extrude(r, (27, 4, -10), 'YZ', "sketch().push([(4, -10)]).circle(12).finalize()", -39, False)
r=extrude(r, (88, 8, -8), 'YZ', "sketch().push([(8, -8)]).circle(10).finalize()", 1)
r=extrude(r, (39, 4, 1), 'YZ', "sketch().segment((0, 0), (0, 8)).segment((0, 14)).segment((0, 16)).segment((0, 22)).segment((8, 22)).segment((8, 14)).segment((8, 8)).segment((8, 6)).segment((8, 0)).arc((4, 1), (0, 0)).assemble().finalize()", 26)
r=extrude(r, (10, -10, -10), 'ZX', "sketch().push([(-10, 10)]).rect(18, 4).finalize()", -9)
r=extrude(r, (65, 7, 7), 'ZX', "sketch().push([(7, 82)]).rect(12, 34).finalize()", 4)
