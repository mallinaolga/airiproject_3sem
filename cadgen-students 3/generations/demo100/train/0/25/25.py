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
r=extrude(r, (-25, 0, 0), 'YZ', "sketch().arc((-21, -31), (-97, 9), (-16, 38)).arc((97, -4), (-21, -31)).assemble().finalize()", 125)
r=extrude(r, (-25, 75, -23), 'YZ', "sketch().segment((85, -11), (86, -18)).segment((90, -18)).arc((62, -32), (85, -11)).assemble().finalize()", -75)
