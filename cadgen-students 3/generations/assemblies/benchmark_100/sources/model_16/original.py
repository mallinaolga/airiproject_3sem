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
r=extrude(r, (0, -86, 0), 'ZX', "sketch().push([(4, 17)]).circle(30).finalize()", 183)
r=extrude(r, (17, -35, 4), 'ZX', "sketch().push([(4, 17)]).circle(41).finalize()", 37, False)
r=extrude(r, (-22, -25, 4), 'ZX', "sketch().segment((-14, -43), (-14, -17)).arc((4, -22), (22, -17)).segment((22, -43)).close().assemble().finalize()", -42)
r=extrude(r, (17, -68, 34), 'ZX', "sketch().arc((24, -4), (34, 17), (24, 38)).segment((40, 26)).arc((49, 29), (58, 26)).arc((61, 17), (58, 8)).arc((49, 5), (40, 8)).close().assemble().finalize()", -29)
r=extrude(r, (-33, -51, -14), 'XY', "sketch().push([(-33, -51)]).circle(25).finalize()", -38)
r=extrude(r, (17, 87, -26), 'XY', "sketch().push([(17, 87)]).rect(16, 14).finalize()", -35)
