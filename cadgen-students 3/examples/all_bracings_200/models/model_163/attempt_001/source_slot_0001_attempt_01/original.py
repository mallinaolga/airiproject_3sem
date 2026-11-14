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
r=extrude(r, (0, -12, 0), 'ZX', "sketch().push([(26, -23)]).circle(23).finalize()", -101)
r=extrude(r, (-23, -65, 26), 'ZX', "sketch().push([(26, -23)]).circle(36).finalize()", -42, False)
r=extrude(r, (0, -24, 26), 'ZX', "sketch().segment((9, -8), (17, 7)).arc((13, 16), (17, 25)).arc((26, 29), (35, 25)).arc((39, 16), (35, 7)).segment((43, -8)).arc((26, 0), (9, -8)).assemble().finalize()", 39)
r=extrude(r, (-1, -24, 19), 'XY', "sketch().push([(-1, 45)]).rect(68, 138).finalize()", -114)
r=extrude(r, (-23, -91, 63), 'ZX', "sketch().arc((52, -48), (63, -23), (52, 2)).segment((76, -5)).arc((94, 2), (112, -5)).arc((119, -23), (112, -41)).arc((94, -48), (76, -41)).close().assemble().finalize()", 81)
r=extrude(r, (34, 69, -91), 'YZ', "sketch().push([(69, -91)]).circle(28).finalize()", 26)
