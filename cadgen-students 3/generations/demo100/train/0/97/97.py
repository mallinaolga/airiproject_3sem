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
r=extrude(r, (0, -100, 0), 'ZX', "sketch().segment((-30, -19), (12, 33)).arc((20, 26), (30, 19)).segment((-12, -33)).close().assemble().finalize()", 92)
r=extrude(r, (-22, -8, -10), 'ZX', "sketch().push([(-10, -22)]).circle(4).finalize()", 108)
