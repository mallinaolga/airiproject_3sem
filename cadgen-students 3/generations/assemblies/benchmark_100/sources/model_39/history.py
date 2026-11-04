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
r=extrude(r, (83, 0, 0), 'YZ', "sketch().push([(2, -6)]).circle(23).finalize()", -198)
r=extrude(r, (77, 2, -6), 'YZ', "sketch().push([(2, -6)]).circle(32).finalize()", -38, False)
r=extrude(r, (-51, 2, 16), 'YZ', "sketch().segment((-9, 13), (-5, 21)).arc((-8, 28), (-5, 35)).arc((2, 38), (9, 35)).arc((12, 28), (9, 21)).segment((13, 13)).arc((2, 16), (-9, 13)).assemble().finalize()", 86)
r=extrude(r, (-8, -20, -6), 'ZX', "sketch().push([(-6, -8)]).rect(44, 52).push([(-6, -8)]).circle(20, mode='s').finalize()", -14)
r=extrude(r, (83, 3, 5), 'ZX', "sketch().segment((-9, 83), (-5, 92)).arc((-9, 102), (-5, 112)).arc((5, 116), (15, 112)).arc((19, 102), (15, 92)).segment((19, 83)).close().assemble().finalize()", 14)
