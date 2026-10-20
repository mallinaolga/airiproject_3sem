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
r=extrude(r, (0, 50, 0), 'ZX', "sketch().segment((-57, 15), (-32, 92)).segment((100, 48)).segment((91, 22)).segment((84, 22)).segment((84, 19)).segment((90, 19)).segment((70, -43)).segment((6, -21)).arc((-73, -85), (-57, 15)).assemble().finalize()", -98)
r=extrude(r, (-64, -48, -45), 'ZX', "sketch().arc((-33, -80), (-66, -62), (-30, -51)).segment((-24, -51)).segment((-24, -80)).close().assemble().finalize()", -2)
