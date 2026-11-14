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
r=extrude(r, (0, -80, 0), 'ZX', "sketch().push([(4, 0)]).circle(12).finalize()", 172)
r=extrude(r, (0, 16, 4), 'ZX', "sketch().push([(4, 0)]).circle(18).finalize()", 26, False)
r=extrude(r, (0, -55, -8), 'XY', "sketch().push([(0, -55)]).circle(2).finalize()", -3)
r=extrude(r, (0, -78, -8), 'XY', "sketch().segment((-25, -63), (25, -74)).segment((8, -93)).close().assemble().finalize()", -16)
r=extrude(r, (0, 36, 22), 'XY', "sketch().push([(0, 36)]).rect(20, 64).finalize()", 2)
