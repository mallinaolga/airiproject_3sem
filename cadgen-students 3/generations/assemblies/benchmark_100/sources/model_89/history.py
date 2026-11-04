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
r=extrude(r, (0, -68, 0), 'ZX', "sketch().push([(5, 20)]).circle(13).finalize()", 168)
r=extrude(r, (20, 14, 5), 'ZX', "sketch().push([(5, 20)]).circle(16).finalize()", 73, False)
r=extrude(r, (7, -18, 5), 'ZX', "sketch().segment((-3, -28), (-3, 11)).arc((5, 7), (13, 11)).segment((13, -28)).close().assemble().finalize()", -53)
r=extrude(r, (20, 28, 21), 'ZX', "sketch().arc((18, 12), (21, 20), (18, 28)).segment((29, 26)).arc((35, 28), (40, 26)).arc((43, 20), (40, 14)).arc((35, 12), (29, 14)).close().assemble().finalize()", -52)
r=extrude(r, (-27, -51, 0), 'YZ', "sketch().push([(-51, 0)]).circle(48).finalize()", -8)
