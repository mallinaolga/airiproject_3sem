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
r=extrude(r, (-107, 0, 0), 'YZ', "sketch().push([(0, 2)]).rect(22, 18).finalize()", 214)
r=extrude(r, (-86, 0, 2), 'YZ', "sketch().push([(0, 2)]).rect(24, 18).finalize()", 23, False)
r=extrude(r, (-87, -11, -4), 'XY', "sketch().push([(-87, 0)]).rect(2, 22).finalize()", -2)
r=extrude(r, (-89, 11, 8), 'XY', "sketch().segment((-92, 11), (-86, 11)).segment((-87, 8)).arc((-86, 6), (-87, 4)).arc((-89, 3), (-91, 4)).arc((-92, 6), (-91, 8)).close().assemble().finalize()", 7)
r=extrude(r, (-44, -4, 11), 'XY', "sketch().segment((-87, -6), (-87, -2)).segment((-65, -2)).segment((-65, 3)).segment((-23, 3)).segment((-23, -2)).segment((-1, -2)).segment((-1, -6)).segment((-23, -6)).segment((-23, -11)).segment((-65, -11)).segment((-65, -6)).close().assemble().finalize()", 11)
r=extrude(r, (8, -11, -6), 'YZ', "sketch().segment((-11, -22), (-11, 10)).segment((-3, -22)).close().assemble().finalize()", -11)
