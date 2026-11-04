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
r=extrude(r, (0, 120, 0), 'ZX', "sketch().push([(0, -26)]).circle(16).finalize()", -240)
r=extrude(r, (-26, 66, 0), 'ZX', "sketch().push([(0, -26)]).circle(20).finalize()", -28, False)
r=extrude(r, (-6, 56, 0), 'YZ', "sketch().push([(56, 0)]).circle(24).finalize()", 52)
r=extrude(r, (-26, -11, 16), 'XY', "sketch().push([(-26, -11)]).rect(40, 16).finalize()", 2)
