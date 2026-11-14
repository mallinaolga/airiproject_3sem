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
r=extrude(r, (63, 0, 0), 'YZ', "sketch().push([(-24, 15)]).rect(76, 44).finalize()", -179)
r=extrude(r, (1, -24, 15), 'YZ', "sketch().push([(-24, 15)]).rect(112, 64).finalize()", -18, False)
r=extrude(r, (40, -29, 35), 'XY', "sketch().push([(40, -29)]).circle(2).finalize()", 25)
r=extrude(r, (52, 14, 30), 'YZ', "sketch().segment((14, 1), (14, 59)).segment((30, 51)).arc((51, 59), (71, 51)).arc((80, 30), (71, 9)).arc((51, 1), (30, 9)).close().assemble().push([(74, 35)]).circle(1, mode='s').finalize()", 64)
r=extrude(r, (-69, 7, 35), 'XY', "sketch().segment((-94, -2), (-94, 16)).segment((-81, 16)).segment((-81, 18)).segment((-57, 18)).segment((-57, 16)).segment((-44, 16)).segment((-44, -2)).segment((-57, -2)).segment((-57, -4)).segment((-81, -4)).segment((-81, -2)).close().assemble().finalize()", 15)
r=extrude(r, (-15, -26, -17), 'XY', "sketch().push([(-15, -26)]).circle(1).finalize()", -43)
