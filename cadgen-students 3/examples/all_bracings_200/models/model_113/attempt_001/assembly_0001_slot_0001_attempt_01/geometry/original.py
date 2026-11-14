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
r=extrude(r, (77, 0, 0), 'YZ', "sketch().push([(7, 0)]).circle(17).finalize()", -153)
r=extrude(r, (-5, 7, 0), 'YZ', "sketch().push([(7, 0)]).circle(20).finalize()", -44, False)
r=extrude(r, (-30, -13, 0), 'ZX', "sketch().push([(0, -30)]).rect(148, 138).finalize()", -6)
r=extrude(r, (77, 6, 14), 'XY', "sketch().segment((77, -33), (77, 45)).segment((81, 45)).segment((79, 35)).segment((99, -33)).close().assemble().finalize()", -45)
r=extrude(r, (-59, -13, -48), 'ZX', "sketch().push([(-48, -59)]).rect(30, 14).finalize()", 82)
r=extrude(r, (77, 16, -23), 'YZ', "sketch().segment((11, -24), (11, -23)).segment((21, -22)).segment((21, -23)).close().assemble().finalize()", -11)
r=extrude(r, (38, -15, -74), 'YZ', "sketch().segment((-69, -74), (-30, -63)).arc((-36, -48), (-30, -34)).arc((-15, -27), (0, -34)).arc((6, -48), (0, -63)).segment((39, -74)).close().assemble().finalize()", 48)
