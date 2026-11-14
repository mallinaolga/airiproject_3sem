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
r=extrude(r, (0, 0, 76), 'XY', "sketch().push([(2, -5)]).circle(15).finalize()", -168)
r=extrude(r, (2, -5, 29), 'XY', "sketch().push([(2, -5)]).circle(25).finalize()", -36, False)
r=extrude(r, (-4, 7, 76), 'XY', "sketch().push([(-4, 7)]).rect(46, 20).finalize()", 16)
r=extrude(r, (9, 15, 28), 'XY', "sketch().push([(9, 15)]).circle(5).finalize()", 39)
r=extrude(r, (9, 19, 40), 'ZX', "sketch().segment((29, 2), (42, 22)).segment((51, 16)).segment((38, -4)).close().assemble().finalize()", 10)
r=extrude(r, (2, 10, -32), 'ZX', "sketch().push([(-32, 2)]).circle(16).push([(-32, 2)]).circle(3, mode='s').finalize()", 3)
