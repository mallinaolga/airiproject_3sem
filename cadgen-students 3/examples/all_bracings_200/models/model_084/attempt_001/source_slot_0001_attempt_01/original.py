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
r=extrude(r, (0, 0, -118), 'XY', "sketch().push([(-6.5, 15)]).rect(55, 64).finalize()", 236)
r=extrude(r, (-7, 15, -64), 'XY', "sketch().push([(-7, 15)]).rect(64, 76).finalize()", 30, False)
r=extrude(r, (-34, -5, -97), 'XY', "sketch().push([(-14, -5)]).rect(40, 98).finalize()", 38)
r=extrude(r, (-6, 47, -92), 'ZX', "sketch().push([(-92, -6)]).circle(10).finalize()", 1)
r=extrude(r, (21, -3, -14), 'YZ', "sketch().push([(-3, -14)]).circle(5).finalize()", 15)
r=extrude(r, (21, 41, 46), 'YZ', "sketch().push([(41, 46)]).circle(3).finalize()", 16)
r=extrude(r, (21, -7, 82), 'YZ', "sketch().push([(-7, 82)]).circle(2).finalize()", 19)
