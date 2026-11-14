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
r=extrude(r, (37, 0, 0), 'YZ', "sketch().push([(-6.5, -1)]).rect(49, 4).finalize()", -131)
r=extrude(r, (-8, -7, -1), 'YZ', "sketch().push([(-7, -1)]).rect(80, 6).finalize()", -19, False)
r=extrude(r, (4, 5, -3), 'YZ', "sketch().segment((-37, -3), (47, -3)).segment((19, -13)).arc((25, -28), (19, -42)).arc((5, -48), (-9, -42)).arc((-15, -28), (-9, -13)).close().assemble().finalize()", 91)
r=extrude(r, (17, 25, -3), 'XY', "sketch().push([(17, 25)]).circle(9).finalize()", 68)
r=extrude(r, (-75, 3, -3), 'XY', "sketch().push([(-75, 3)]).rect(8, 2).finalize()", -62)
