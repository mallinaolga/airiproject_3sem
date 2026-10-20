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
r=extrude(r, (0, -17, 0), 'ZX', "sketch().segment((-100, 25), (-100, 26)).segment((100, 26)).arc((87, 8), (69, -7)).segment((67, -16)).segment((58, -14)).arc((44, -19), (29, -23)).arc((-36, -19), (-87, 21)).close().assemble().finalize()", 52)
r=extrude(r, (23, -17, 49), 'ZX', "sketch().push([(49, 23)]).circle(2).finalize()", -19)
