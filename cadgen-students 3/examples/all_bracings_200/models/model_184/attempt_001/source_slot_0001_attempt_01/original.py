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
r=extrude(r, (71, 0, 0), 'YZ', "sketch().push([(3, -17)]).circle(25).finalize()", -162)
r=extrude(r, (-34, 3, -17), 'YZ', "sketch().push([(3, -17)]).circle(43).finalize()", -19, False)
r=extrude(r, (-16, 3, 8), 'YZ', "sketch().segment((-18, -4), (-12, 20)).arc((-18, 35), (-12, 50)).arc((3, 56), (18, 50)).arc((24, 35), (18, 20)).segment((24, -4)).arc((3, 8), (-18, -4)).assemble().finalize()", 55)
r=extrude(r, (57, -22, -17), 'ZX', "sketch().push([(-17, 57)]).circle(50).finalize()", -7)
r=extrude(r, (-85, -22, -17), 'ZX', "sketch().push([(-17, -85)]).circle(22).finalize()", -24)
r=extrude(r, (-52, 3, 27), 'XY', "sketch().push([(-52, 3)]).circle(27).push([(-32, 11)]).circle(2, mode='s').finalize()", 40)
