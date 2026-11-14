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
r=extrude(r, (0, 113, 0), 'ZX', "sketch().push([(4, 0)]).circle(11).finalize()", -206)
r=extrude(r, (0, -90, 4), 'ZX', "sketch().push([(4, 0)]).circle(15).finalize()", -24, False)
r=extrude(r, (0, 41, -7), 'XY', "sketch().push([(0, 41)]).rect(30, 48).finalize()", -12)
r=extrude(r, (0, -57, -7), 'XY', "sketch().segment((-10, -50), (-3, -49)).arc((-1, -48), (0, -48)).segment((8, -47)).segment((10, -64)).segment((3, -65)).arc((1, -66), (0, -66)).segment((-8, -67)).close().assemble().finalize()", -2)
r=extrude(r, (0, -49, -8), 'XY', "sketch().segment((-5, -51), (-3, -37)).arc((-5, -34), (-3, -30)).arc((0, -29), (3, -30)).arc((5, -34), (3, -37)).segment((5, -51)).arc((0, -49), (-5, -51)).assemble().push([(0, -34)]).circle(2, mode='s').finalize()", -4)
