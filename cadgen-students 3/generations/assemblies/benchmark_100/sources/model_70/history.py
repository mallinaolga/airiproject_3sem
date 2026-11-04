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
r=extrude(r, (0, 0, -62), 'XY', "sketch().push([(-8.5, -1)]).rect(21, 50).finalize()", 179)
r=extrude(r, (-8, -1, -61), 'XY', "sketch().push([(-8, -1)]).rect(30, 72).finalize()", 69, False)
r=extrude(r, (0, -26, -62), 'XY', "sketch().push([(0, -26)]).circle(20).finalize()", -24)
r=extrude(r, (20, -26, -68), 'YZ', "sketch().push([(-26, -68)]).circle(12).finalize()", 3)
r=extrude(r, (0, -46, -73), 'ZX', "sketch().arc((-117, 2), (-75, 7), (-40, 29)).segment((-29, -2)).segment((-106, -29)).close().assemble().finalize()", -3)
r=extrude(r, (7, -25, -24), 'YZ', "sketch().push([(-25, -24)]).rect(6, 14).finalize()", 9)
r=extrude(r, (-13, 33, -61), 'XY', "sketch().push([(-13, 33)]).circle(16).finalize()", -28)
