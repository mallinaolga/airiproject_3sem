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
r=extrude(r, (0, -97, 0), 'ZX', "sketch().push([(0, -2)]).circle(10).finalize()", 193)
r=extrude(r, (-2, -13, 0), 'ZX', "sketch().push([(0, -2)]).circle(15).finalize()", 36, False)
r=extrude(r, (13, -11, 0), 'YZ', "sketch().push([(-11, 0)]).circle(8).finalize()", 5)
