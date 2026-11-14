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
r=extrude(r, (0, 0, -61), 'XY', "sketch().push([(36, 0)]).circle(26).finalize()", 109)
r=extrude(r, (36, 0, -14), 'XY', "sketch().push([(36, 0)]).circle(32).finalize()", 15, False)
r=extrude(r, (10, 0, 44), 'YZ', "sketch().push([(0, 44)]).circle(55).finalize()", -84)
r=extrude(r, (32, 2, -61), 'ZX', "sketch().arc((-93, 20), (-98, 32), (-93, 44)).arc((-81, 49), (-70, 44)).segment((-61, 74)).segment((-61, -10)).segment((-70, 20)).arc((-81, 15), (-93, 20)).assemble().push([(-81, 32)]).circle(14, mode='s').finalize()", 21)
