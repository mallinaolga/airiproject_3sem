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
r=extrude(r, (-106, 0, 0), 'YZ', "sketch().push([(41, 0)]).rect(6, 30).finalize()", 213)
r=extrude(r, (-34, 41, 0), 'YZ', "sketch().push([(41, 0)]).rect(8, 38).finalize()", 29, False)
r=extrude(r, (-69, 39, 7), 'YZ', "sketch().push([(-3, 7)]).rect(84, 6).finalize()", 3)
r=extrude(r, (-7, 45, 0), 'ZX', "sketch().push([(0, -7)]).circle(11).finalize()", 1)
r=extrude(r, (-67, 32, 9), 'YZ', "sketch().push([(32, 9)]).rect(10, 10).finalize()", 5)
r=extrude(r, (-67, 30, 12), 'XY', "sketch().push([(-84.5, 30)]).rect(35, 4).finalize()", -26)
