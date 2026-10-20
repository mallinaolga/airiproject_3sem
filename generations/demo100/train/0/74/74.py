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
r=extrude(r, (0, 0, 37), 'XY', "sketch().arc((-15, -39), (-17, 33), (17, -31)).arc((19, -99), (-15, -39)).assemble().finalize()", -43)
r=extrude(r, (-7, 34, -2), 'XY', "sketch().segment((-29, 26), (-29, 100)).segment((15, 100)).segment((15, 26)).arc((-7, 34), (-29, 26)).assemble().finalize()", -29)
r=extrude(r, (-21, 9, -6), 'XY', "sketch().segment((-21, 4), (-21, 7)).arc((-22, 13), (-18, 8)).segment((-18, 4)).close().assemble().finalize()", -31)
