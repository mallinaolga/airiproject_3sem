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
r=extrude(r, (0, 0, 70), 'XY', "sketch().push([(-3.5, 11)]).rect(33, 26).finalize()", -164)
r=extrude(r, (-3, 11, -74), 'XY', "sketch().push([(-3, 11)]).rect(42, 32).finalize()", -17, False)
r=extrude(r, (13, 20, 49), 'XY', "sketch().arc((-15, 10), (-19, 20), (-15, 30)).arc((-5, 34), (6, 30)).segment((13, 44)).segment((13, -4)).segment((6, 10)).arc((-5, 6), (-15, 10)).assemble().finalize()", -9)
r=extrude(r, (5, -5, -88), 'ZX', "sketch().push([(-88, 5)]).rect(2, 2).finalize()", -15)
r=extrude(r, (11, -2, 54), 'ZX', "sketch().push([(54, 11)]).rect(80, 26).finalize()", -41)
