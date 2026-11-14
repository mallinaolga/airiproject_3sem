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
r=extrude(r, (53, 0, 0), 'YZ', "sketch().push([(-5, 11)]).circle(14).finalize()", -154)
r=extrude(r, (20, -5, 11), 'YZ', "sketch().push([(-5, 11)]).circle(24).finalize()", -66, False)
r=extrude(r, (19, -23, 0), 'ZX', "sketch().push([(0, 60)]).rect(106, 82).finalize()", -5)
r=extrude(r, (-17, -5, -13), 'YZ', "sketch().arc((-16, -9), (-5, -13), (6, -9)).segment((3, -27)).arc((6, -35), (3, -42)).arc((-5, -45), (-13, -42)).arc((-16, -35), (-13, -27)).close().assemble().finalize()", 53)
r=extrude(r, (-61, 8, 11), 'ZX', "sketch().segment((6, -64), (7, -57)).segment((13, -58)).segment((16, -58)).segment((15, -65)).segment((9, -64)).close().assemble().finalize()", 21)
