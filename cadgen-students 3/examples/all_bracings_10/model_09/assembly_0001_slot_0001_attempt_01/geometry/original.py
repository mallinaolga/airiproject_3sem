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
r=extrude(r, (0, 98, 0), 'ZX', "sketch().push([(2.5, -11)]).rect(5, 38).finalize()", -196)
r=extrude(r, (-12, -53, 2), 'ZX', "sketch().push([(2, -12)]).rect(8, 66).finalize()", -23, False)
r=extrude(r, (-36, -72, -2), 'XY', "sketch().push([(-36, -72)]).rect(24, 24).finalize()", -4)
r=extrude(r, (1, 74, 4), 'XY', "sketch().segment((-13, 73), (-3, 88)).segment((15, 75)).segment((5, 60)).close().assemble().push([(1, 74)]).circle(1, mode='s').finalize()", 10)
r=extrude(r, (6, -84, 0), 'YZ', "sketch().segment((-94, -17), (-94, 17)).segment((-74, 17)).arc((-83, 0), (-74, -17)).close().assemble().finalize()", 42)
