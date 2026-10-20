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
r=extrude(r, (0, 0, -17), 'XY', "sketch().arc((-79, -12), (-65, 15), (-59, -15)).segment((-59, 6)).segment((-79, 6)).close().assemble().finalize()", 117)
r=extrude(r, (-57, -1, -17), 'XY', "sketch().segment((-58, -6), (-58, 4)).arc((-56, -1), (-58, -6)).assemble().finalize()", -83)
r=extrude(r, (-51, -1, 76), 'XY', "sketch().arc((-58, -14), (-51, -1), (-58, 12)).segment((83, 12)).segment((83, -14)).close().assemble().finalize()", -37)
r=extrude(r, (-58, -12, -17), 'XY', "sketch().push([(-58, -12)]).rect(2, 2).finalize()", -82)
