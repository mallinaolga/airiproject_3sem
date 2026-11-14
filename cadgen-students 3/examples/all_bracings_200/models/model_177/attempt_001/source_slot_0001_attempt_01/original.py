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
r=extrude(r, (34, 0, 0), 'YZ', "sketch().push([(-4, -17)]).circle(8).finalize()", -143)
r=extrude(r, (-53, -4, -17), 'YZ', "sketch().push([(-4, -17)]).circle(10).finalize()", -29, False)
r=extrude(r, (-2, -4, -9), 'YZ', "sketch().segment((-10, -12), (-8, -5)).arc((-10, -1), (-8, 4)).arc((-4, 5), (0, 4)).arc((2, -1), (0, -5)).segment((2, -12)).arc((-4, -9), (-10, -12)).assemble().finalize()", 103)
r=extrude(r, (100, 0, 1), 'YZ', "sketch().segment((-25, -7), (-7, 26)).segment((25, 9)).segment((7, -24)).close().assemble().finalize()", 9)
r=extrude(r, (-40, -12, -17), 'ZX', "sketch().segment((-26, -45), (-25, -33)).segment((-8, -35)).segment((-9, -47)).close().assemble().finalize()", -12)
