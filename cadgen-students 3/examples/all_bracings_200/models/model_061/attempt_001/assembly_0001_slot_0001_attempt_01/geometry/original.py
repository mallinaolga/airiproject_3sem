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
r=extrude(r, (96, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(36, 24).finalize()", -176)
r=extrude(r, (-78, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(52, 36).finalize()", -18, False)
r=extrude(r, (7, -18, 1), 'ZX', "sketch().arc((-4, 11), (-3, 13), (0, 13)).arc((4, 1), (-4, 11)).assemble().finalize()", -8)
r=extrude(r, (86, -18, 1), 'ZX', "sketch().push([(1, 86)]).circle(3).finalize()", -6)
r=extrude(r, (-41, -18, -4), 'ZX', "sketch().push([(-4, -41)]).rect(6, 14).finalize()", -3)
