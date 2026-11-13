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
r=extrude(r, (101, 0, 0), 'YZ', "sketch().push([(-4.5, 0)]).rect(25, 38).finalize()", -201)
r=extrude(r, (-63, -4, 0), 'YZ', "sketch().push([(-4, 0)]).rect(26, 42).finalize()", -25, False)
r=extrude(r, (-57, 8, -14), 'ZX', "sketch().push([(-14, -57)]).circle(1).finalize()", 16)
r=extrude(r, (-41, -17, -17), 'ZX', "sketch().segment((-18, -41), (-17, -40)).segment((-16, -41)).segment((-17, -42)).close().assemble().finalize()", -10)
r=extrude(r, (-25, 3, 19), 'YZ', "sketch().segment((-8, 19), (14, 19)).segment((11, 12)).arc((14, 5), (11, -3)).arc((3, -6), (-5, -3)).arc((-8, 5), (-5, 12)).close().assemble().finalize()", 28)
r=extrude(r, (37, 8, -5), 'ZX', "sketch().arc((-17, 33), (3, 47), (-6, 24)).arc((-10, 30), (-17, 33)).assemble().finalize()", 18)
