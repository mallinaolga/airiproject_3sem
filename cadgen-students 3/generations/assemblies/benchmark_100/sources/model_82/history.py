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
r=extrude(r, (-118, 0, 0), 'YZ', "sketch().push([(14, 0)]).circle(12).finalize()", 209)
r=extrude(r, (89, 14, 0), 'YZ', "sketch().push([(14, 0)]).circle(14).finalize()", 30, False)
r=extrude(r, (108, 1, 0), 'YZ', "sketch().arc((-15, -6), (-18, 0), (-15, 6)).arc((-9, 8), (-4, 6)).segment((4, 8)).arc((1, 0), (4, -8)).segment((-4, -6)).arc((-9, -8), (-15, -6)).assemble().finalize()", -188)
r=extrude(r, (11, -18, 0), 'ZX', "sketch().segment((-25, -2), (-18, 33)).segment((25, 24)).segment((18, -11)).close().assemble().finalize()", -5)
r=extrude(r, (0, -23, 11), 'ZX', "sketch().push([(11, 0)]).rect(12, 6).finalize()", -5)
