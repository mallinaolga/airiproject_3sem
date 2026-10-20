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
r=extrude(r, (0, -77, 0), 'ZX', "sketch().arc((-50, -100), (-40, 18), (73, -17)).arc((-9, -28), (-50, -100)).assemble().finalize()", 154)
r=extrude(r, (31, -7, 3), 'YZ', "sketch().segment((-62, -17), (-62, 66)).segment((48, 66)).segment((48, -60)).segment((-9, -60)).segment((-9, -29)).segment((-10, -29)).segment((-10, -17)).close().assemble().push([(-7, 3)]).circle(4, mode='s').finalize()", 69)
