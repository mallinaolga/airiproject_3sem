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
r=extrude(r, (0, 107, 0), 'ZX', "sketch().push([(23, -29.5)]).rect(46, 33).finalize()", -214)
r=extrude(r, (-29, -16, 23), 'ZX', "sketch().push([(23, -29)]).rect(72, 52).finalize()", -37, False)
r=extrude(r, (-13, 50, 35), 'XY', "sketch().push([(21.5, 50)]).rect(69, 12).finalize()", -63)
r=extrude(r, (-46, -69, 29), 'YZ', "sketch().push([(-69, 29)]).rect(42, 38).finalize()", -3)
r=extrude(r, (-42, 64, 0), 'XY', "sketch().push([(-42, 64)]).rect(2, 2).finalize()", -9)
r=extrude(r, (-34, 67, 0), 'XY', "sketch().push([(-34, 67)]).circle(7).finalize()", -60)
