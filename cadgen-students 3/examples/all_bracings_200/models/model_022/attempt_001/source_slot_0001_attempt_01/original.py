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
r=extrude(r, (0, 0, -78), 'XY', "sketch().push([(-2, 0)]).circle(16).finalize()", 191)
r=extrude(r, (-2, 0, -30), 'XY', "sketch().push([(-2, 0)]).circle(19).finalize()", 24, False)
r=extrude(r, (-18, 0, 85), 'XY', "sketch().segment((-25, -13), (-25, 13)).segment((-11, 13)).arc((-18, 0), (-11, -13)).close().assemble().finalize()", -50)
r=extrude(r, (14, 0, 106), 'YZ', "sketch().segment((-12, 113), (7, 118)).segment((12, 99)).segment((-7, 94)).close().assemble().finalize()", 3)
r=extrude(r, (-13, -3, -78), 'ZX', "sketch().push([(-98, -13)]).rect(40, 14).finalize()", 1)
r=extrude(r, (14, 0, -50), 'YZ', "sketch().push([(0, -50)]).circle(12).finalize()", 11)
