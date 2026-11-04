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
r=extrude(r, (0, 0, -60), 'XY', "sketch().push([(0, 0)]).circle(13).finalize()", 148)
r=extrude(r, (0, 0, 75), 'XY', "sketch().push([(0, 0)]).circle(20).finalize()", 16, False)
r=extrude(r, (-10, -7, -60), 'XY', "sketch().push([(-10, -7)]).rect(4, 2).finalize()", -32)
r=extrude(r, (-2, 11, -60), 'XY', "sketch().push([(-2, 11)]).rect(30, 26).finalize()", -5)
r=extrude(r, (1, 0, -65), 'YZ', "sketch().push([(0, -76.5)]).rect(42, 23).finalize()", -9)
r=extrude(r, (-13, 0, 26), 'YZ', "sketch().segment((-29, -9), (-10, 70)).segment((29, 61)).segment((10, -18)).close().assemble().finalize()", -7)
