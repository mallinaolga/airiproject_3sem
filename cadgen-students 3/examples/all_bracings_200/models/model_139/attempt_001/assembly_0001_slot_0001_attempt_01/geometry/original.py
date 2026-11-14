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
r=extrude(r, (0, 104, 0), 'ZX', "sketch().push([(15.5, -9)]).rect(17, 52).finalize()", -209)
r=extrude(r, (-9, 67, 15), 'ZX', "sketch().push([(15, -9)]).rect(18, 54).finalize()", -25, False)
r=extrude(r, (-28, 67, 24), 'YZ', "sketch().segment((67, 14), (67, 34)).segment((80, 31)).arc((87, 34), (94, 31)).arc((97, 24), (94, 17)).arc((87, 14), (80, 17)).close().assemble().finalize()", 35)
r=extrude(r, (12, 58, 6), 'XY', "sketch().push([(12, 58)]).rect(48, 34).finalize()", -40)
r=extrude(r, (0, 4, 24), 'XY', "sketch().push([(0, 4)]).rect(12, 2).finalize()", 9)
