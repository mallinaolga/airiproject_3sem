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
r=extrude(r, (0, -91, 0), 'ZX', "sketch().push([(2, -1.5)]).rect(10, 23).finalize()", 187)
r=extrude(r, (-1, 0, 2), 'ZX', "sketch().push([(2, -1)]).rect(10, 24).finalize()", 20, False)
r=extrude(r, (-13, 43, 1), 'YZ', "sketch().segment((40, 17), (45, 17)).arc((43, -15), (40, 17)).assemble().finalize()", -8)
r=extrude(r, (9, -91, 3), 'ZX', "sketch().segment((-7, 18), (16, 25)).segment((21, 9)).segment((0, 3)).arc((-13, -4), (-4, 8)).close().assemble().finalize()", -5)
r=extrude(r, (-21, 42, -6), 'YZ', "sketch().push([(42, -6)]).circle(15).finalize()", -4)
r=extrude(r, (-8, -62, 7), 'XY', "sketch().push([(-8, -62)]).rect(2, 2).finalize()", 14)
r=extrude(r, (5, 12, 7), 'XY', "sketch().push([(5, 12)]).circle(1).finalize()", 8)
