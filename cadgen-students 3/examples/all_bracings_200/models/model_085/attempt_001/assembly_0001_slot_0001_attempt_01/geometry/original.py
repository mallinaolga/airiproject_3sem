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
r=extrude(r, (-96, 0, 0), 'YZ', "sketch().push([(-7.5, 15.5)]).rect(23, 3).finalize()", 193)
r=extrude(r, (-12, -7, 15), 'YZ', "sketch().push([(-7, 15)]).rect(26, 2).finalize()", 26, False)
r=extrude(r, (-55, 0, 16), 'XY', "sketch().push([(-55, 0)]).rect(12, 60).finalize()", 7)
r=extrude(r, (-60, 30, 19), 'ZX', "sketch().push([(19, -60)]).circle(17).finalize()", 1)
r=extrude(r, (-64, -12, 16), 'XY', "sketch().push([(-64, -12)]).rect(2, 2).finalize()", 10)
r=extrude(r, (28, -11, 14), 'XY', "sketch().push([(28, -11)]).circle(12).finalize()", -50)
