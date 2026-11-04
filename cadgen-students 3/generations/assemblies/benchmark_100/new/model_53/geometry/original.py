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
r=extrude(r, (-101, 0, 0), 'YZ', "sketch().push([(25, -17.5)]).rect(52, 41).finalize()", 218)
r=extrude(r, (-7, 25, -18), 'YZ', "sketch().push([(25, -18)]).rect(62, 50).finalize()", 36, False)
r=extrude(r, (-96, 40, 2), 'XY', "sketch().segment((-117, 49), (-95, 63)).segment((-75, 31)).segment((-97, 17)).close().assemble().finalize()", 41)
r=extrude(r, (-35, 0, -27), 'ZX', "sketch().push([(-27, -35)]).circle(1).finalize()", -62)
