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
r=extrude(r, (0, -112, 0), 'ZX', "sketch().push([(15.5, -0.5)]).rect(75, 17).finalize()", 192)
r=extrude(r, (0, 48, 15), 'ZX', "sketch().push([(15, 0)]).rect(128, 30).finalize()", 63, False)
r=extrude(r, (14, 58, 33), 'YZ', "sketch().push([(58, 33)]).circle(5).finalize()", 8)
r=extrude(r, (14, 50, 0), 'YZ', "sketch().push([(50, 0)]).rect(70, 208).finalize()", 9)
r=extrude(r, (-15, 94, 32), 'YZ', "sketch().push([(94, 32)]).circle(7).finalize()", -8)
