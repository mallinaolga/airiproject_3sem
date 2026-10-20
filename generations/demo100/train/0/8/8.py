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
r=extrude(r, (0, 44, 0), 'ZX', "sketch().segment((-100, -64), (-100, 1)).segment((28, 1)).segment((28, 64)).segment((100, 64)).segment((100, -17)).segment((39, -17)).segment((39, -64)).close().assemble().push([(64, 24)]).circle(13, mode='s').finalize()", -88)
