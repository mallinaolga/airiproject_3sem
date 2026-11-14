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
r=extrude(r, (60, 0, 0), 'YZ', "sketch().push([(48, -35)]).circle(30).finalize()", -151)
r=extrude(r, (34, 48, -35), 'YZ', "sketch().push([(48, -35)]).circle(38).finalize()", -31, False)
r=extrude(r, (33, 21, -57), 'ZX', "sketch().segment((-59, 33), (-58, 40)).arc((-59, 41), (-58, 42)).arc((-57, 43), (-56, 42)).arc((-55, 41), (-56, 40)).segment((-55, 33)).close().assemble().finalize()", -101)
r=extrude(r, (43, -80, -57), 'ZX', "sketch().segment((-58, 42), (-58, 91)).segment((-56, 91)).segment((-56, 42)).arc((-57, 43), (-58, 42)).assemble().finalize()", -6)
r=extrude(r, (9, 48, 3), 'YZ', "sketch().segment((23, -7), (23, 74)).segment((73, 74)).segment((73, -7)).arc((48, 3), (23, -7)).assemble().finalize()", -10)
r=extrude(r, (43, 18, -35), 'ZX', "sketch().push([(-35, 43)]).circle(4).finalize()", -9)
