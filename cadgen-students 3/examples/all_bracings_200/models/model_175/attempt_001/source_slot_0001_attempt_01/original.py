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
r=extrude(r, (0, 118, 0), 'ZX', "sketch().push([(3, 0)]).circle(20).finalize()", -207)
r=extrude(r, (0, -70, 3), 'ZX', "sketch().push([(3, 0)]).circle(24).finalize()", -49, False)
r=extrude(r, (0, 14, -16), 'XY', "sketch().segment((-45, 11), (-45, 17)).segment((-43, 17)).arc((0, 57), (43, 17)).segment((45, 17)).segment((45, 11)).segment((43, 11)).arc((0, -29), (-43, 11)).close().assemble().finalize()", -17)
r=extrude(r, (20, 83, 3), 'YZ', "sketch().push([(83, 3)]).rect(16, 24).finalize()", 18)
r=extrude(r, (-22, -19, -16), 'XY', "sketch().push([(-22, -19)]).circle(2).finalize()", 50)
