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
r=extrude(r, (0, -89, 0), 'ZX', "sketch().push([(-1, -0.5)]).rect(12, 15).finalize()", 143)
r=extrude(r, (-1, -59, -1), 'ZX', "sketch().push([(-1, -1)]).rect(20, 26).finalize()", 44, False)
r=extrude(r, (7, -71, -5), 'ZX', "sketch().segment((-11, 7), (1, 7)).segment((-1, 3)).arc((1, -1), (-1, -5)).arc((-5, -6), (-9, -5)).arc((-11, -1), (-9, 3)).close().assemble().finalize()", -10)
r=extrude(r, (-8, 0, 3), 'XY', "sketch().push([(-5, 0)]).rect(6, 202).finalize()", 1)
r=extrude(r, (0, -19, 9), 'XY', "sketch().push([(0, -19)]).rect(28, 26).finalize()", 2)
