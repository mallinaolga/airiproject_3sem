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
r=extrude(r, (0, 12, 0), 'ZX', "sketch().push([(14, -46)]).circle(6).finalize()", -37)
r=extrude(r, (-46, 0, 14), 'ZX', "sketch().push([(14, -46)]).circle(9).finalize()", -12, False)
r=extrude(r, (-37, -10, 14), 'YZ', "sketch().segment((-63, 22), (-8, 52)).segment((0, 69)).segment((25, 58)).segment((20, 48)).segment((43, 6)).segment((-12, -24)).segment((-20, -41)).segment((-45, -30)).segment((-40, -20)).close().assemble().finalize()", 58)
r=extrude(r, (21, 6, 1), 'YZ', "sketch().push([(6, 1)]).rect(28, 2).finalize()", 22)
r=extrude(r, (22, -7, 0), 'YZ', "sketch().segment((-7, -71), (-7, 71)).segment((20, 37)).arc((57, 52), (94, 37)).arc((109, 0), (94, -37)).arc((57, -52), (20, -37)).close().assemble().finalize()", 5)
r=extrude(r, (41, 8, 0), 'ZX', "sketch().segment((0, 27), (0, 55)).segment((13, 51)).arc((23, 55), (32, 51)).arc((36, 41), (32, 31)).arc((23, 27), (13, 31)).close().assemble().finalize()", -117)
