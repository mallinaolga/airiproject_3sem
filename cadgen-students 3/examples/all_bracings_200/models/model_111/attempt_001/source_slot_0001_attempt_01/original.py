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
r=extrude(r, (0, 0, -42), 'XY', "sketch().push([(-29, 13)]).circle(34).finalize()", 110)
r=extrude(r, (-29, 13, -6), 'XY', "sketch().push([(-29, 13)]).circle(43).finalize()", 14, False)
r=extrude(r, (-34, 20, 68), 'XY', "sketch().push([(-34, 20)]).circle(24).finalize()", 27)
r=extrude(r, (4, 13, 18), 'XY', "sketch().arc((-9, -12), (4, 13), (-9, 38)).segment((94, 38)).segment((94, -12)).close().assemble().finalize()", 22)
r=extrude(r, (-29, -19, -34), 'ZX', "sketch().push([(-34, -29)]).rect(122, 130).finalize()", -36)
