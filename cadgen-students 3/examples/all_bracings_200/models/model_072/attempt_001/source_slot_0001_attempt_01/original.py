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
r=extrude(r, (0, -118, 0), 'ZX', "sketch().push([(-7.5, -2)]).rect(37, 2).finalize()", 235)
r=extrude(r, (-2, -73, -8), 'ZX', "sketch().push([(-8, -2)]).rect(64, 4).finalize()", 24, False)
r=extrude(r, (-4, -64, -30), 'YZ', "sketch().push([(-64, -30)]).circle(4).finalize()", -26)
r=extrude(r, (-3, -73, 18), 'ZX', "sketch().push([(18, -3)]).circle(1).finalize()", -30)
r=extrude(r, (0, -50, 24), 'XY', "sketch().push([(0, -50)]).rect(104, 60).finalize()", 15)
