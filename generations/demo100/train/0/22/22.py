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
r=extrude(r, (0, 61, 0), 'ZX', "sketch().segment((-57, -87), (-57, -31)).segment((-54, -35)).segment((55, 87)).segment((55, -87)).close().assemble().finalize()", 39)
r=extrude(r, (42, 61, 55), 'ZX', "sketch().push([(55, 42)]).circle(2).finalize()", -161)
