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
r=extrude(r, (0, -92, 0), 'ZX', "sketch().push([(14, -38.5)]).rect(38, 5).finalize()", 141)
r=extrude(r, (-38, 21, 15), 'ZX', "sketch().push([(15, -38)]).rect(56, 8).finalize()", 39, False)
r=extrude(r, (-35, 34, -3), 'XY', "sketch().segment((-35, -24), (-35, 92)).segment((-17, 58)).arc((7, 68), (31, 58)).arc((42, 34), (31, 10)).arc((7, 0), (-17, 10)).close().assemble().finalize()", -21)
r=extrude(r, (-36, 0, 18), 'YZ', "sketch().push([(0, 18)]).rect(2, 10).finalize()", 72)
r=extrude(r, (-37, 33, -14), 'XY', "sketch().push([(-37, 33)]).circle(2).finalize()", -29)
r=extrude(r, (21, -2, 16), 'ZX', "sketch().push([(16, 21)]).rect(52, 36).finalize()", -64)
