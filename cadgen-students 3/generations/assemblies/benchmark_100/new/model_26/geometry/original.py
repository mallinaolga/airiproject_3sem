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
r=extrude(r, (0, -76, 0), 'ZX', "sketch().push([(-6, -8.5)]).rect(40, 15).finalize()", 126)
r=extrude(r, (-9, -73, -6), 'ZX', "sketch().push([(-6, -9)]).rect(60, 20).finalize()", 34, False)
r=extrude(r, (-2, -68, -35), 'XY', "sketch().push([(-2, -68)]).rect(2, 2).finalize()", -11)
r=extrude(r, (-16, 0, -8), 'XY', "sketch().segment((-16, -110), (-16, 110)).segment((-7, 12)).arc((5, 17), (17, 12)).arc((22, 0), (17, -12)).arc((5, -17), (-7, -12)).close().assemble().finalize()", 19)
r=extrude(r, (17, 5, 10), 'XY', "sketch().push([(17, 5)]).rect(6, 12).finalize()", 37)
r=extrude(r, (-16, 70, -1), 'YZ', "sketch().push([(70, -1)]).rect(6, 8).finalize()", -23)
r=extrude(r, (21, 0, -2), 'YZ', "sketch().push([(0, -2)]).rect(24, 68).finalize()", 18)
