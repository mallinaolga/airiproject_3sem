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
r=extrude(r, (0, 0, 93), 'XY', "sketch().push([(7.5, 2)]).rect(29, 30).finalize()", -207)
r=extrude(r, (8, 2, 9), 'XY', "sketch().push([(8, 2)]).rect(40, 42).finalize()", -60, False)
r=extrude(r, (7, -11, 32), 'ZX', "sketch().push([(32, 7)]).circle(4).finalize()", -12)
r=extrude(r, (-7, 5, 93), 'XY', "sketch().segment((-28, 10), (9, 19)).segment((14, 0)).segment((-23, -9)).close().assemble().finalize()", 21)
r=extrude(r, (-1, 19, -103), 'ZX', "sketch().push([(-103, -1)]).circle(5).finalize()", 1)
