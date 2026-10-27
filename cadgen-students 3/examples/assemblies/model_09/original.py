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
r=extrude(r, (62, 0, 0), 'YZ', "sketch().push([(-14, 68)]).circle(17).finalize()", -129)
r=extrude(r, (-28, -14, 68), 'YZ', "sketch().push([(-14, 68)]).circle(23).finalize()", -18, False)
r=extrude(r, (-49, 3, 68), 'YZ', "sketch().arc((-5, 55), (3, 68), (-5, 81)).segment((14, 78)).arc((23, 81), (33, 78)).arc((37, 68), (33, 58)).arc((23, 55), (14, 58)).close().assemble().finalize()", -63)
r=extrude(r, (62, -23, 75), 'YZ', "sketch().push([(-23, 75)]).circle(5).finalize()", 50)
r=extrude(r, (-20, -14, 51), 'XY', "sketch().push([(-20, -14)]).circle(1).finalize()", -143)
