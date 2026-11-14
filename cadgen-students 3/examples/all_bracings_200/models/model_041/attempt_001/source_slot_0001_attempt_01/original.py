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
r=extrude(r, (0, 83, 0), 'ZX', "sketch().push([(-10, -16)]).circle(15).finalize()", -189)
r=extrude(r, (-16, 9, -10), 'ZX', "sketch().push([(-10, -16)]).circle(23).finalize()", -70, False)
r=extrude(r, (7, -24, -10), 'YZ', "sketch().arc((-7, -47), (-46, 25), (2, -42)).arc((-5, -41), (-7, -47)).assemble().finalize()", 35)
r=extrude(r, (41, -43, 0), 'YZ', "sketch().push([(-43, 0)]).circle(64).finalize()", 20)
r=extrude(r, (-16, 62, -24), 'XY', "sketch().push([(-16, 62)]).circle(45).finalize()", -7)
