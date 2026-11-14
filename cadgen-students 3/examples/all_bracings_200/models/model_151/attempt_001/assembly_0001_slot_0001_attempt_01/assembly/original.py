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
r=extrude(r, (0, 0, 90), 'XY', "sketch().push([(0, 2)]).circle(10).finalize()", -196)
r=extrude(r, (0, 2, 77), 'XY', "sketch().push([(0, 2)]).circle(13).finalize()", -20, False)
r=extrude(r, (-1, 8, 90), 'XY', "sketch().segment((-8, 4), (-8, 5)).segment((6, 12)).segment((6, 11)).close().assemble().finalize()", 16)
r=extrude(r, (0, -8, -66), 'ZX', "sketch().push([(-66, 0)]).circle(10).finalize()", -4)
r=extrude(r, (0, -8, -36), 'XY', "sketch().segment((-5, -15), (-5, -6)).arc((0, -8), (5, -6)).segment((5, -15)).close().assemble().finalize()", 48)
r=extrude(r, (0, 1, 90), 'XY', "sketch().push([(0, 1)]).circle(6).finalize()", 7)
r=extrude(r, (0, -5, 96), 'XY', "sketch().arc((-4, -3), (0, -5), (4, -3)).segment((2, -7)).arc((3, -9), (2, -11)).arc((0, -12), (-2, -11)).arc((-3, -9), (-2, -7)).close().assemble().finalize()", 4)
