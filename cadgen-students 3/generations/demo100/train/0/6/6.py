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
r=extrude(r, (0, 0, -95), 'XY', "sketch().push([(10, 0)]).rect(36, 168).push([(0, 0)]).circle(11, mode='s').finalize()", 195)
r=extrude(r, (-2, 0, 3), 'XY', "sketch().segment((-28, -9), (-28, 9)).segment((3, 9)).arc((-2, 0), (3, -9)).close().assemble().finalize()", -103)
