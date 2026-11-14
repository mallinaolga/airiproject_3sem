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
r=extrude(r, (0, 89, 0), 'ZX', "sketch().push([(-17, 4)]).circle(24).finalize()", -195)
r=extrude(r, (4, 6, -17), 'ZX', "sketch().push([(-17, 4)]).circle(25).finalize()", -37, False)
r=extrude(r, (1, 89, 5), 'ZX', "sketch().push([(5, 1)]).circle(1).finalize()", 17)
r=extrude(r, (-20, 62, -17), 'ZX', "sketch().segment((-33, -29), (-33, -14)).arc((-17, -20), (-1, -14)).segment((-1, -29)).close().assemble().finalize()", 39)
r=extrude(r, (3, 89, -27), 'ZX', "sketch().segment((-36, -4), (-26, 15)).segment((-18, 10)).segment((-28, -9)).close().assemble().finalize()", 4)
r=extrude(r, (4, 37, 6), 'XY', "sketch().segment((8, 41), (12, 41)).segment((12, 35)).segment((9, 35)).arc((-4, 36), (8, 41)).assemble().finalize()", 36)
