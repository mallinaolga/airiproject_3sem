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
r=extrude(r, (0, 101, 0), 'ZX', "sketch().push([(55, 0)]).circle(29).finalize()", -159)
r=extrude(r, (0, -34, 55), 'ZX', "sketch().push([(55, 0)]).circle(49).finalize()", -20, False)
r=extrude(r, (0, -48, 6), 'XY', "sketch().push([(0, -48)]).circle(37).finalize()", -114)
r=extrude(r, (-13, -67, -107), 'XY', "sketch().push([(-13, -67)]).circle(34).finalize()", -7)
r=extrude(r, (-6, -34, 99), 'ZX', "sketch().segment((84, -47), (84, 35)).segment((114, -47)).close().assemble().finalize()", 15)
