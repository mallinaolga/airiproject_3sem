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
r=extrude(r, (0, -19, 0), 'ZX', "sketch().push([(14, 0)]).circle(53).push([(0, 0)]).circle(8, mode='s').finalize()", 119)
r=extrude(r, (-20, -19, -30), 'ZX', "sketch().arc((-67, 9), (-22, -10), (7, -49)).close().assemble().finalize()", -81)
