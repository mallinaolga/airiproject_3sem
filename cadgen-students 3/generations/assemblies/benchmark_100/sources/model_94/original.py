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
r=extrude(r, (0, 0, -99), 'XY', "sketch().push([(0, 0)]).circle(17).finalize()", 198)
r=extrude(r, (0, 0, -19), 'XY', "sketch().push([(0, 0)]).circle(26).finalize()", 50, False)
r=extrude(r, (10, -20, -19), 'XY', "sketch().push([(10, -20)]).rect(2, 6).finalize()", -36)
r=extrude(r, (0, 17, 95), 'ZX', "sketch().segment((94, -5), (94, 5)).arc((96, 0), (94, -5)).assemble().finalize()", 1)
r=extrude(r, (0, 17, 55), 'ZX', "sketch().push([(55, 0)]).circle(2).finalize()", 3)
