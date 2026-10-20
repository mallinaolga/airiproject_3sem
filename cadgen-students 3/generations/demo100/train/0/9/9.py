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
r=extrude(r, (0, -16, 0), 'ZX', "sketch().push([(0, -12)]).circle(39).finalize()", 20)
r=extrude(r, (0, -16, 19), 'XY', "sketch().segment((-100, -16), (-10, -9)).arc((-14, 1), (-10, 12)).arc((0, 16), (10, 12)).arc((14, 1), (10, -9)).segment((100, -16)).close().assemble().finalize()", -5)
