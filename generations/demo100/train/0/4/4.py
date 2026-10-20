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
r=extrude(r, (0, 100, 0), 'ZX', "sketch().segment((-91, -67), (-91, 40)).segment((-31, 40)).segment((-31, 65)).segment((29, 67)).segment((29, 40)).segment((91, 40)).segment((91, -67)).close().assemble().finalize()", -200)
