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
r=extrude(r, (0, 98, 0), 'ZX', "sketch().push([(-7, 0)]).circle(13).finalize()", -205)
r=extrude(r, (0, 96, -7), 'ZX', "sketch().push([(-7, 0)]).circle(20).finalize()", -29, False)
r=extrude(r, (5, 98, -8), 'ZX', "sketch().push([(-8, 5)]).circle(20).finalize()", 10)
r=extrude(r, (0, 77, 13), 'XY', "sketch().push([(0, 77)]).rect(6, 26).finalize()", 16)
r=extrude(r, (0, -12, -20), 'XY', "sketch().push([(0, -12)]).rect(48, 6).finalize()", -8)
