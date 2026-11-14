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
r=extrude(r, (-96, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(24).finalize()", 184)
r=extrude(r, (-26, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(37).finalize()", 50, False)
r=extrude(r, (67, -24, 0), 'ZX', "sketch().push([(0, 67)]).rect(70, 22).finalize()", -1)
r=extrude(r, (-27, 9, 31), 'YZ', "sketch().push([(9, 31)]).circle(2).finalize()", -41)
r=extrude(r, (83, 24, 0), 'ZX', "sketch().push([(0, 83)]).circle(13).finalize()", 13)
