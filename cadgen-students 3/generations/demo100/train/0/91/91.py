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
r=extrude(r, (0, 42, 0), 'ZX', "sketch().segment((-100, -34), (-100, 72)).segment((29, 72)).segment((29, 69)).segment((61, 79)).segment((100, -43)).segment((-15, -79)).segment((-29, -34)).close().assemble().push([(23, 0)]).circle(52, mode='s').finalize()", -84)
