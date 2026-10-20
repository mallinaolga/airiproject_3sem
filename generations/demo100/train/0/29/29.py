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
r=extrude(r, (0, 16, 0), 'ZX', "sketch().segment((-81, -37), (-81, 68)).segment((81, 68)).segment((81, -37)).segment((65, -37)).segment((65, -68)).segment((-54, -68)).segment((-54, -37)).close().assemble().finalize()", -99)
r=extrude(r, (68, 0, 31), 'XY', "sketch().arc((8, -22), (-1, 0), (8, 22)).arc((30, 31), (52, 22)).segment((68, 100)).segment((68, -100)).segment((52, -22)).arc((30, -31), (8, -22)).assemble().push([(30, 0)]).circle(27, mode='s').finalize()", -34)
