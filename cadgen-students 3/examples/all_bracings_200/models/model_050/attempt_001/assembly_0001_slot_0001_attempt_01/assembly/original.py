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
r=extrude(r, (0, 0, 105), 'XY', "sketch().push([(-4.5, 12)]).rect(57, 30).finalize()", -215)
r=extrude(r, (-5, 12, 87), 'XY', "sketch().push([(-5, 12)]).rect(84, 44).finalize()", -24, False)
r=extrude(r, (12, -10, 75), 'ZX', "sketch().push([(75, 12)]).circle(35).finalize()", -26)
r=extrude(r, (-27, 34, 79), 'ZX', "sketch().push([(79, -27)]).rect(6, 26).finalize()", 13)
r=extrude(r, (-2, -36, 80), 'ZX', "sketch().push([(80, -2)]).rect(6, 76).finalize()", -11)
r=extrude(r, (-23, -43, 83), 'XY', "sketch().push([(-23, -43)]).circle(2).finalize()", 7)
