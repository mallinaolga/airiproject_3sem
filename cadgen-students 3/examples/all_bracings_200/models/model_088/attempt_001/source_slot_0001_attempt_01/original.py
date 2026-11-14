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
r=extrude(r, (0, 0, 32), 'XY', "sketch().push([(-21, -49)]).circle(4).finalize()", 15)
r=extrude(r, (-21, -49, 43), 'XY', "sketch().push([(-21, -49)]).circle(5).finalize()", 2, False)
r=extrude(r, (-16, -49, 33), 'XY', "sketch().arc((-18, -52), (-16, -49), (-18, -46)).segment((8, -46)).segment((8, -52)).close().assemble().finalize()", -85)
r=extrude(r, (-21, -45, 47), 'ZX', "sketch().segment((-4, -54), (-4, -47)).segment((6, -47)).segment((6, 7)).segment((-4, 7)).segment((-4, 12)).segment((98, 12)).segment((98, -54)).close().assemble().finalize()", 47)
r=extrude(r, (4, -52, -9), 'XY', "sketch().segment((-46, -52), (-30, -27)).arc((-44, 7), (-30, 41)).arc((4, 55), (38, 41)).arc((52, 7), (38, -27)).segment((54, -52)).close().assemble().finalize()", -89)
r=extrude(r, (-10, -46, -6), 'ZX', "sketch().push([(-6, -10)]).circle(1).finalize()", 48)
