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
r=extrude(r, (0, 93, 0), 'ZX', "sketch().push([(-1, 1)]).circle(46).finalize()", -168)
r=extrude(r, (1, -36, -1), 'ZX', "sketch().push([(-1, 1)]).circle(63).finalize()", -58, False)
r=extrude(r, (1, 64, 45), 'ZX', "sketch().arc((39, -20), (45, 1), (39, 22)).segment((118, 22)).segment((118, -20)).close().assemble().finalize()", -5)
r=extrude(r, (1, 72, -47), 'ZX', "sketch().segment((-118, -12), (-118, 14)).segment((-44, 14)).arc((-47, 1), (-44, -12)).close().assemble().finalize()", -32)
r=extrude(r, (-20, 61, 100), 'YZ', "sketch().push([(61, 100)]).rect(34, 34).finalize()", -44)
r=extrude(r, (-12, 53, -116), 'YZ', "sketch().push([(53, -116)]).rect(2, 2).finalize()", -19)
