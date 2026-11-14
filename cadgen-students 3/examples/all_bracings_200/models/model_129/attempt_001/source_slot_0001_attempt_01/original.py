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
r=extrude(r, (0, 96, 0), 'ZX', "sketch().push([(-36.5, 0)]).rect(5, 34).finalize()", -192)
r=extrude(r, (0, -18, -36), 'ZX', "sketch().push([(-36, 0)]).rect(8, 56).finalize()", -74, False)
r=extrude(r, (18, -64, -32), 'XY', "sketch().segment((14, -81), (20, -47)).segment((22, -47)).segment((16, -81)).close().assemble().finalize()", 8)
r=extrude(r, (17, 18, -34), 'YZ', "sketch().push([(18, -34)]).rect(2, 2).finalize()", 3)
r=extrude(r, (-3, 18, -34), 'XY', "sketch().segment((-14, 28), (-6, 33)).segment((8, 8)).segment((0, 3)).close().assemble().finalize()", 5)
r=extrude(r, (-7, -45, -32), 'XY', "sketch().push([(-7, -45)]).circle(3).finalize()", 73)
r=extrude(r, (-9, 82, -34), 'XY', "sketch().push([(-9, 82)]).circle(6).finalize()", 34)
