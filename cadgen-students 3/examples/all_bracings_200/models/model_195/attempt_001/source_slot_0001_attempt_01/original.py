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
r=extrude(r, (-85, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(41).finalize()", 164)
r=extrude(r, (51, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(54).finalize()", 42, False)
r=extrude(r, (8, -41, 0), 'YZ', "sketch().segment((-64, -33), (-64, 33)).segment((-23, 33)).arc((-41, 0), (-23, -33)).close().assemble().finalize()", 4)
r=extrude(r, (-52, 41, 0), 'ZX', "sketch().push([(0, -52)]).rect(28, 28).finalize()", 23)
r=extrude(r, (-50, 0, 41), 'XY', "sketch().push([(-50, 0)]).rect(84, 20).finalize()", 3)
