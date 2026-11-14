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
r=extrude(r, (0, 0, 78), 'XY', "sketch().push([(10, -63)]).circle(40).finalize()", -178)
r=extrude(r, (10, -63, 55), 'XY', "sketch().push([(10, -63)]).circle(43).finalize()", -22, False)
r=extrude(r, (10, -23, -8), 'XY', "sketch().segment((-16, -33), (-16, 87)).segment((36, 87)).segment((36, -33)).arc((10, -23), (-16, -33)).assemble().finalize()", 29)
r=extrude(r, (13, 87, 4), 'ZX', "sketch().push([(4, 13)]).circle(16).finalize()", 20)
r=extrude(r, (16, 36, 21), 'XY', "sketch().segment((9, 35), (9, 37)).segment((14, 37)).segment((14, 36)).segment((15, 36)).segment((15, 37)).segment((23, 37)).segment((23, 35)).close().assemble().finalize()", 19)
r=extrude(r, (36, 25, -6), 'YZ', "sketch().segment((-4, 6), (17, 6)).segment((54, -10)).segment((51, -18)).close().assemble().finalize()", 11)
r=extrude(r, (-30, -63, -47), 'YZ', "sketch().push([(-63, -47)]).circle(1).finalize()", -42)
r=extrude(r, (-16, 86, 20), 'XY', "sketch().push([(28, 86)]).rect(88, 34).finalize()", 80)
