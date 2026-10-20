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
r=extrude(r, (0, 0, -70), 'XY', "sketch().segment((-78, 73), (15, 100)).segment((23, 75)).arc((66, 46), (85, -3)).segment((93, -3)).segment((93, -69)).segment((64, -69)).arc((-63, -78), (-71, 49)).close().assemble().finalize()", 141)
