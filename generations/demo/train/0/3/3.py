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
r=extrude(r, (-100, 0, 0), 'YZ', "sketch().segment((-56, -77), (-32, -43)).arc((-47, -19), (-46, 9)).arc((-34, 79), (31, 49)).segment((47, 72)).segment((58, 65)).segment((35, 31)).arc((42, -34), (-21, -50)).segment((-45, -84)).close().assemble().finalize()", 200)
