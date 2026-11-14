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
r=extrude(r, (0, 0, 108), 'XY', "sketch().push([(7, -31.5)]).rect(20, 29).finalize()", -225)
r=extrude(r, (7, -32, -47), 'XY', "sketch().push([(7, -32)]).rect(24, 34).finalize()", -39, False)
r=extrude(r, (0, -22, 18), 'YZ', "sketch().push([(-22, 18)]).rect(28, 86).finalize()", -19)
r=extrude(r, (3, -16, 5), 'YZ', "sketch().push([(16.5, 5)]).rect(65, 222).finalize()", 11)
r=extrude(r, (0, -33, -95), 'YZ', "sketch().push([(-33, -95)]).circle(4).finalize()", -7)
r=extrude(r, (3, -5, 87), 'YZ', "sketch().segment((-10, 88), (-5, 92)).segment((0, 86)).segment((-5, 82)).close().assemble().finalize()", -10)
