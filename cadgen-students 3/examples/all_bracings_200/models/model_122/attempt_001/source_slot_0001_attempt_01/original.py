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
r=extrude(r, (0, 0, -116), 'XY', "sketch().push([(44, 0)]).circle(16).finalize()", 199)
r=extrude(r, (44, 0, 50), 'XY', "sketch().push([(44, 0)]).circle(22).finalize()", 66, False)
r=extrude(r, (44, -16, 32), 'ZX', "sketch().push([(32, 44)]).rect(24, 26).finalize()", -53)
r=extrude(r, (31, -29, 22), 'YZ', "sketch().segment((-30, 22), (-29, 23)).segment((-28, 22)).segment((-29, 21)).close().assemble().finalize()", -97)
r=extrude(r, (21, 0, 76), 'XY', "sketch().arc((2, -6), (-1, 0), (2, 6)).arc((8, 9), (15, 6)).segment((24, 9)).arc((21, 0), (24, -9)).segment((15, -6)).arc((8, -9), (2, -6)).assemble().finalize()", -70)
r=extrude(r, (21, 0, 26), 'YZ', "sketch().segment((-92, 37), (61, 95)).segment((92, 15)).segment((-61, -43)).close().assemble().push([(0, 26)]).circle(40, mode='s').finalize()", -36)
