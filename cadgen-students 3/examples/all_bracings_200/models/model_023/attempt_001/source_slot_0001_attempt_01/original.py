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
r=extrude(r, (0, 0, 73), 'XY', "sketch().push([(1, -17)]).circle(22).finalize()", -140)
r=extrude(r, (1, -17, 27), 'XY', "sketch().push([(1, -17)]).circle(35).finalize()", -45, False)
r=extrude(r, (23, -40, 27), 'XY', "sketch().push([(23, -40)]).circle(2).finalize()", 58)
r=extrude(r, (1, 18, -18), 'ZX', "sketch().segment((-92, 23), (-74, 45)).segment((-5, -13)).segment((56, -13)).segment((56, -34)).segment((-7, -34)).segment((-14, -43)).close().assemble().finalize()", 32)
r=extrude(r, (37, -17, 4), 'YZ', "sketch().push([(-17, 4)]).circle(6).finalize()", 3)
r=extrude(r, (-21, 29, 57), 'XY', "sketch().push([(-21, 29)]).circle(24).push([(-21, 29)]).circle(21, mode='s').finalize()", 35)
r=extrude(r, (23, -17, -51), 'YZ', "sketch().push([(-17, -51)]).rect(12, 30).finalize()", 15)
