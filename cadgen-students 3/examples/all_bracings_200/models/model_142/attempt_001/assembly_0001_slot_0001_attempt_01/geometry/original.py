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
r=extrude(r, (0, 0, -98), 'XY', "sketch().push([(-29, 40)]).circle(38).finalize()", 159)
r=extrude(r, (-29, 40, 59), 'XY', "sketch().push([(-29, 40)]).circle(63).finalize()", 29, False)
r=extrude(r, (-29, 2, -69), 'ZX', "sketch().push([(-69, -29)]).rect(4, 2).finalize()", -101)
r=extrude(r, (-29, 2, -86), 'ZX', "sketch().push([(-86, -29)]).circle(4).finalize()", -105)
r=extrude(r, (34, 40, 67), 'YZ', "sketch().push([(40, 67)]).rect(58, 62).finalize()", 58)
