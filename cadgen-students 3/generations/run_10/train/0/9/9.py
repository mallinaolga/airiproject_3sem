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
r=extrude(r, (0, 0, -21), 'XY', "sketch().push([(-7, 2.5)]).rect(146, 101).finalize()", 38)
r=extrude(r, (-73, -3, 0), 'ZX', "sketch().push([(0, -58)]).rect(200, 30).finalize()", -6)
