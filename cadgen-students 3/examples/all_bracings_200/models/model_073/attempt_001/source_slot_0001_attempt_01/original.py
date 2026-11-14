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
r=extrude(r, (93, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(26, 26).finalize()", -186)
r=extrude(r, (-15, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(34, 34).finalize()", -22, False)
r=extrude(r, (-19, 10, 18), 'XY', "sketch().push([(-19, 10)]).circle(3).finalize()", 4)
r=extrude(r, (-27, -6, -17), 'XY', "sketch().segment((-30, -6), (-30, -4)).segment((-29, -4)).arc((-28, -3), (-27, -3)).segment((-25, -3)).segment((-25, -5)).arc((-24, -5), (-24, -6)).segment((-24, -8)).segment((-25, -8)).arc((-26, -9), (-27, -9)).segment((-29, -9)).segment((-29, -7)).arc((-30, -7), (-30, -6)).assemble().finalize()", -9)
r=extrude(r, (-68, 10, 13), 'XY', "sketch().push([(-68, 10)]).circle(3).finalize()", 13)
