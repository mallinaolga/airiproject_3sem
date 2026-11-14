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
r=extrude(r, (0, 75, 0), 'ZX', "sketch().push([(0, 3)]).circle(14).finalize()", -121)
r=extrude(r, (3, -42, 0), 'ZX', "sketch().push([(0, 3)]).circle(16).finalize()", -31, False)
r=extrude(r, (17, 51, 0), 'YZ', "sketch().segment((43, 24), (45, 25)).segment((59, -24)).segment((57, -25)).close().assemble().finalize()", 1)
r=extrude(r, (13, 75, 3), 'ZX', "sketch().push([(3, 13)]).circle(2).finalize()", 17)
r=extrude(r, (-13, -51, 0), 'YZ', "sketch().segment((-92, -19), (-92, 8)).segment((-63, 8)).segment((-63, 30)).segment((-21, 30)).segment((-21, 8)).segment((-10, 8)).segment((-10, -19)).segment((-21, -19)).segment((-21, -30)).segment((-63, -30)).segment((-63, -19)).close().assemble().finalize()", -6)
r=extrude(r, (9, 75, -9), 'ZX', "sketch().segment((-11, 7), (-10, 11)).segment((-7, 11)).segment((-8, 7)).close().assemble().finalize()", 9)
r=extrude(r, (17, 47, 16), 'ZX', "sketch().segment((13, 17), (19, 17)).segment((18, 12)).arc((19, 10), (18, 8)).arc((16, 7), (14, 8)).arc((13, 10), (14, 12)).close().assemble().finalize()", -3)
