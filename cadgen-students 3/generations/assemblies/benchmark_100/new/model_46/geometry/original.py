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
r=extrude(r, (0, 0, 103), 'XY', "sketch().push([(-12, 4.5)]).rect(10, 25).finalize()", -207)
r=extrude(r, (-12, 5, -49), 'XY', "sketch().push([(-12, 5)]).rect(18, 42).finalize()", -24, False)
r=extrude(r, (-15, 25, -56), 'ZX', "sketch().push([(-56, -15)]).circle(3).push([(-56, -14)]).circle(1, mode='s').finalize()", 10)
r=extrude(r, (-8, 9, -21), 'XY', "sketch().segment((-8, -9), (-8, 27)).segment((-1, 18)).arc((8, 22), (17, 18)).arc((20, 9), (17, 0)).arc((8, -4), (-1, 0)).close().assemble().push([(-2, 8)]).circle(2, mode='s').finalize()", 31)
r=extrude(r, (8, -4, 7), 'XY', "sketch().segment((-2, -36), (-2, 2)).arc((8, -4), (18, 2)).segment((18, -36)).close().assemble().finalize()", 23)
