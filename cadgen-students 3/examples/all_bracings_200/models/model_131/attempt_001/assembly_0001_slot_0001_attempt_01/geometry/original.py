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
r=extrude(r, (0, 0, 116), 'XY', "sketch().push([(0, 0)]).rect(28, 14).finalize()", -232)
r=extrude(r, (0, 0, -77), 'XY', "sketch().push([(0, 0)]).rect(44, 24).finalize()", -24, False)
r=extrude(r, (12, 4, 76), 'XY', "sketch().segment((12, -2), (12, 10)).segment((14, 7)).arc((17, 8), (20, 7)).arc((21, 4), (20, 1)).arc((17, 0), (14, 1)).close().assemble().finalize()", 25)
