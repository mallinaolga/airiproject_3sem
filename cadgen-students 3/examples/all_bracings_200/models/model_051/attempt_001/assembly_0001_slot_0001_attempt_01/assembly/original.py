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
r=extrude(r, (0, 0, 86), 'XY', "sketch().push([(4.5, -7)]).rect(35, 16).finalize()", -186)
r=extrude(r, (4, -7, -88), 'XY', "sketch().push([(4, -7)]).rect(40, 18).finalize()", -19, False)
r=extrude(r, (-13, -4, 34), 'ZX', "sketch().push([(34, 4.5)]).rect(148, 35).finalize()", 15)
r=extrude(r, (15, 11, -3), 'ZX', "sketch().segment((-5, 16), (-2, 17)).segment((-1, 14)).segment((-4, 13)).close().assemble().finalize()", 5)
r=extrude(r, (-14, 1, -32), 'YZ', "sketch().push([(1, -32)]).rect(4, 2).finalize()", -1)
r=extrude(r, (-16, -5, -90), 'YZ', "sketch().push([(-5, -90)]).circle(1).finalize()", -8)
