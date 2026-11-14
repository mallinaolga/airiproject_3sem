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
r=extrude(r, (-109, 0, 0), 'YZ', "sketch().push([(0, 39)]).circle(11).finalize()", 218)
r=extrude(r, (-88, 0, 39), 'YZ', "sketch().push([(0, 39)]).circle(20).finalize()", 29, False)
r=extrude(r, (14, 0, 28), 'YZ', "sketch().segment((-8, -59), (-8, 32)).arc((0, 28), (8, 32)).segment((8, -59)).close().assemble().finalize()", -22)
r=extrude(r, (42, 11, 39), 'ZX', "sketch().push([(39, 42)]).circle(6).finalize()", 2)
r=extrude(r, (-69, 0, 19), 'XY', "sketch().push([(-69, 0)]).rect(28, 30).push([(-69, 0)]).circle(9, mode='s').finalize()", -46)
