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
r=extrude(r, (0, -58, 0), 'ZX', "sketch().segment((73, -38), (73, 38)).segment((100, -23)).segment((100, -38)).close().assemble().finalize()", 117)
r=extrude(r, (-2, -45, 73), 'XY', "sketch().segment((-5, -47), (-5, -43)).segment((-2, -43)).arc((1, -44), (-1, -45)).segment((-1, -47)).close().assemble().finalize()", -174)
