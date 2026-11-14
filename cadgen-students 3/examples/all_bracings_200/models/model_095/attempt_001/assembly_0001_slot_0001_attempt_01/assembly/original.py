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
r=extrude(r, (-94, 0, 0), 'YZ', "sketch().push([(0, -0.5)]).rect(78, 47).finalize()", 189)
r=extrude(r, (-27, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(126, 74).finalize()", 36, False)
r=extrude(r, (-52, 4, -24), 'XY', "sketch().push([(-52, 4)]).rect(50, 92).finalize()", -20)
r=extrude(r, (-18, -15, 37), 'XY', "sketch().push([(-18, -15)]).circle(1).finalize()", 7)
r=extrude(r, (-63, -42, -38), 'ZX', "sketch().push([(-38, -63)]).circle(2).finalize()", -13)
