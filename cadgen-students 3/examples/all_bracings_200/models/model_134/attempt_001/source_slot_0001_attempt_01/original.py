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
r=extrude(r, (-32, 0, 0), 'YZ', "sketch().push([(0, 7)]).circle(23).finalize()", 124)
r=extrude(r, (12, 0, 7), 'YZ', "sketch().push([(0, 7)]).circle(39).finalize()", 33, False)
r=extrude(r, (-6, 0, -16), 'YZ', "sketch().segment((-12, -46), (-12, -12)).arc((0, -16), (12, -12)).segment((12, -46)).close().assemble().finalize()", 3)
r=extrude(r, (-32, 3, 5), 'XY', "sketch().segment((-91, -10), (-91, 16)).segment((-63, 16)).segment((-73, 13)).segment((-53, 6)).segment((-42, 10)).segment((-58, 16)).segment((-32, 16)).segment((-32, -10)).close().assemble().finalize()", 3)
