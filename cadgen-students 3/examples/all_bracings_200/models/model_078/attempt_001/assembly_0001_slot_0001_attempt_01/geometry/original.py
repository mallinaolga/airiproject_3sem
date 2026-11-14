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
r=extrude(r, (0, -93, 0), 'ZX', "sketch().push([(-6, -15)]).rect(28, 18).finalize()", 186)
r=extrude(r, (-15, -54, -6), 'ZX', "sketch().push([(-6, -15)]).rect(34, 22).finalize()", 44, False)
r=extrude(r, (-6, 24, 0), 'ZX', "sketch().push([(0, 9)]).rect(68, 30).finalize()", -16)
r=extrude(r, (24, 10, 19), 'YZ', "sketch().push([(10, 19)]).circle(1).finalize()", 1)
r=extrude(r, (-17, -7, -20), 'XY', "sketch().push([(-17, -7)]).circle(1).finalize()", -7)
