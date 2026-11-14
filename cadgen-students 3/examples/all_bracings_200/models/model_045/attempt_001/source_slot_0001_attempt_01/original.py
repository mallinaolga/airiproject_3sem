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
r=extrude(r, (0, -105, 0), 'ZX', "sketch().push([(-57, 33)]).circle(12).finalize()", 211)
r=extrude(r, (33, 40, -57), 'ZX', "sketch().push([(-57, 33)]).circle(20).finalize()", 22, False)
r=extrude(r, (33, 98, -46), 'XY', "sketch().push([(33, 98)]).rect(2, 6).finalize()", 136)
r=extrude(r, (53, 46, -57), 'YZ', "sketch().push([(46, -57)]).rect(80, 46).finalize()", 15)
r=extrude(r, (45, 91, -57), 'YZ', "sketch().push([(91, -57)]).circle(7).finalize()", 11)
r=extrude(r, (33, 101, 62), 'YZ', "sketch().push([(101, 62)]).circle(1).finalize()", -100)
r=extrude(r, (33, -13, -69), 'XY', "sketch().push([(33, -13)]).circle(8).finalize()", -21)
