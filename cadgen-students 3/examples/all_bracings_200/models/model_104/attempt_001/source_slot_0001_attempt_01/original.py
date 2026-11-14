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
r=extrude(r, (0, 0, -76), 'XY', "sketch().push([(23, 32)]).circle(11).finalize()", 180)
r=extrude(r, (23, 32, 77), 'XY', "sketch().push([(23, 32)]).circle(17).finalize()", 18, False)
r=extrude(r, (34, 32, 50), 'YZ', "sketch().segment((31, 43), (31, 54)).arc((32, 54), (31, 55)).segment((31, 57)).segment((33, 57)).segment((33, 43)).close().assemble().finalize()", 16)
r=extrude(r, (12, 32, -1), 'YZ', "sketch().push([(32, -1)]).circle(1).finalize()", -62)
r=extrude(r, (23, 21, 16), 'XY', "sketch().segment((15, -48), (15, 26)).arc((23, 21), (31, 26)).segment((31, -48)).close().assemble().finalize()", -120)
