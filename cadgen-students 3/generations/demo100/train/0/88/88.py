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
r=extrude(r, (0, 16, 0), 'ZX', "sketch().segment((-27, 49), (-27, 71)).segment((13, 71)).segment((61, 71)).segment((100, 71)).segment((100, 8)).arc((-27, 2), (100, -4)).segment((100, -67)).segment((61, -67)).segment((13, -67)).segment((-18, -67)).arc((-100, -15), (-27, 49)).assemble().finalize()", -33)
