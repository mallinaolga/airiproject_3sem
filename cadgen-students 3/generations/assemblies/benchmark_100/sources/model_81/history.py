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
r=extrude(r, (0, -111, 0), 'ZX', "sketch().push([(0.5, 5)]).rect(25, 8).finalize()", 229)
r=extrude(r, (5, -77, 1), 'ZX', "sketch().push([(1, 5)]).rect(34, 12).finalize()", 44, False)
r=extrude(r, (-1, -97, -11), 'YZ', "sketch().push([(-97, -11)]).circle(21).finalize()", -30)
r=extrude(r, (1, 89, -14), 'XY', "sketch().push([(1, 89)]).circle(29).finalize()", -10)
r=extrude(r, (-17, -97, 11), 'XY', "sketch().push([(-17, -97)]).rect(14, 6).finalize()", 21)
