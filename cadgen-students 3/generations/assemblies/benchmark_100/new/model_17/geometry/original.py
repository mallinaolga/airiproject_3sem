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
r=extrude(r, (0, 107, 0), 'ZX', "sketch().push([(-4, -4.5)]).rect(18, 27).finalize()", -212)
r=extrude(r, (-5, -24, -4), 'ZX', "sketch().push([(-4, -5)]).rect(28, 46).finalize()", -30, False)
r=extrude(r, (9, -6, -10), 'YZ', "sketch().push([(-6, -10)]).circle(2).finalize()", 2)
r=extrude(r, (-18, 76, -9), 'XY', "sketch().segment((-18, 59), (-18, 93)).segment((-14, 82)).arc((-8, 84), (-2, 82)).arc((1, 76), (-2, 70)).arc((-8, 68), (-14, 70)).close().assemble().finalize()", -10)
r=extrude(r, (16, -41, -19), 'XY', "sketch().segment((4, -43), (27, -36)).segment((28, -39)).segment((5, -46)).close().assemble().finalize()", -2)
r=extrude(r, (-18, -92, 2), 'YZ', "sketch().push([(-92, 2)]).rect(30, 36).finalize()", -10)
