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
r=extrude(r, (105, 0, 0), 'YZ', "sketch().push([(-3, 5.5)]).rect(8, 39).finalize()", -212)
r=extrude(r, (78, -3, 5), 'YZ', "sketch().push([(-3, 5)]).rect(12, 62).finalize()", -71, False)
r=extrude(r, (73, -9, 18), 'ZX', "sketch().push([(18, 73)]).circle(34).finalize()", -25)
r=extrude(r, (59, -3, -26), 'XY', "sketch().push([(59, -3)]).rect(4, 2).finalize()", -5)
r=extrude(r, (-28, 0, -14), 'XY', "sketch().push([(-28, 0)]).circle(54).finalize()", -39)
r=extrude(r, (69, -9, 49), 'ZX', "sketch().push([(49, 69)]).rect(8, 12).finalize()", 11)
