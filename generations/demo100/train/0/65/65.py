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
r=extrude(r, (71, 0, 0), 'YZ', "sketch().segment((-68, -74), (-68, 12)).segment((-27, 12)).arc((10, -8), (47, 12)).segment((57, 12)).segment((57, -74)).close().assemble().push([(-53, -24)]).circle(13, mode='s').finalize()", 29)
r=extrude(r, (71, -23, -62), 'XY', "sketch().segment((-100, -28), (-2, 0)).segment((71, 0)).segment((71, -46)).segment((47, -46)).close().assemble().finalize()", 57)
r=extrude(r, (71, 35, -46), 'XY', "sketch().arc((11, 13), (1, 35), (11, 57)).arc((33, 66), (55, 57)).segment((71, 68)).segment((71, 2)).segment((55, 13)).arc((33, 4), (11, 13)).assemble().finalize()", 120)
