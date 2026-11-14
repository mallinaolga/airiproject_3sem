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
r=extrude(r, (0, 0, -61), 'XY', "sketch().push([(-3, -12)]).rect(56, 62).finalize()", 171)
r=extrude(r, (-3, -12, -12), 'XY', "sketch().push([(-3, -12)]).rect(94, 106).finalize()", 28, False)
r=extrude(r, (-13, 41, 11), 'ZX', "sketch().push([(11, -13)]).rect(4, 34).finalize()", 25)
r=extrude(r, (21, -17, -61), 'XY', "sketch().push([(21, -17)]).circle(3).finalize()", -48)
r=extrude(r, (10, -43, 48), 'XY', "sketch().push([(10, -10)]).rect(2, 66).finalize()", 11)
r=extrude(r, (44, -57, -10), 'YZ', "sketch().push([(-57, -10)]).rect(4, 24).push([(-57, -10)]).circle(1, mode='s').finalize()", 6)
