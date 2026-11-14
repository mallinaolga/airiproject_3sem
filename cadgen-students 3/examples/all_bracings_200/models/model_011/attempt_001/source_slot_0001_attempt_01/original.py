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
r=extrude(r, (-114, 0, 0), 'YZ', "sketch().push([(0, -39)]).circle(18).finalize()", 228)
r=extrude(r, (34, 0, -39), 'YZ', "sketch().push([(0, -39)]).circle(27).finalize()", 67, False)
r=extrude(r, (83, 0, -66), 'XY', "sketch().push([(83, 0)]).circle(17).finalize()", -35)
r=extrude(r, (85, 15, -100), 'XY', "sketch().push([(85, 15)]).circle(8).finalize()", -8)
r=extrude(r, (89, 13, -109), 'XY', "sketch().push([(89, 13)]).rect(2, 4).finalize()", -11)
r=extrude(r, (34, 16, -56), 'YZ', "sketch().segment((13, -57), (15, -54)).segment((19, -55)).segment((17, -58)).close().assemble().finalize()", -133)
r=extrude(r, (-18, 0, -21), 'XY', "sketch().segment((-42, -19), (-15, 31)).segment((6, 19)).segment((-21, -31)).close().assemble().finalize()", 97)
