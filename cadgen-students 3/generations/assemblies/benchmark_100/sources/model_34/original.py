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
r=extrude(r, (0, 0, -75), 'XY', "sketch().push([(-18, 8.5)]).rect(8, 13).finalize()", 94)
r=extrude(r, (-18, 9, -8), 'XY', "sketch().push([(-18, 9)]).rect(12, 20).finalize()", 16, False)
r=extrude(r, (-19, -3, 6), 'ZX', "sketch().push([(6, -19)]).circle(16).finalize()", -21)
r=extrude(r, (-12, -24, 0), 'YZ', "sketch().segment((-24, -93), (-24, 93)).segment((20, 93)).segment((20, -49)).arc((-3, -68), (-24, -93)).assemble().finalize()", 15)
r=extrude(r, (5, -2, -8), 'YZ', "sketch().push([(-2, -8)]).rect(44, 50).finalize()", 14)
r=extrude(r, (3, 21, 76), 'ZX', "sketch().push([(76, 3)]).circle(1).finalize()", 3)
r=extrude(r, (-35, -17, 6), 'YZ', "sketch().push([(-17, 6)]).rect(12, 8).finalize()", -1)
r=extrude(r, (5, 18, -46), 'YZ', "sketch().push([(18, -46)]).rect(4, 8).push([(18, -47)]).circle(1, mode='s').finalize()", 10)
r=extrude(r, (5, -15, 80), 'YZ', "sketch().push([(-15, 80)]).circle(8).finalize()", 32)
