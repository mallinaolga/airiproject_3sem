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
r=extrude(r, (0, 0, -66), 'XY', "sketch().push([(18, 57)]).circle(33).finalize()", 129)
r=extrude(r, (18, 57, 37), 'XY', "sketch().push([(18, 57)]).circle(47).finalize()", 17, False)
r=extrude(r, (-29, 57, 50), 'YZ', "sketch().push([(57, 50)]).circle(1).finalize()", -40)
r=extrude(r, (18, 10, 52), 'ZX', "sketch().push([(52, 18)]).rect(16, 56).finalize()", -100)
r=extrude(r, (40, -90, 48), 'ZX', "sketch().segment((38, 11), (38, 69)).segment((58, 19)).close().assemble().finalize()", -13)
r=extrude(r, (-10, -43, 53), 'YZ', "sketch().push([(-43, 53)]).circle(14).push([(-47, 43)]).circle(2, mode='s').finalize()", -15)
