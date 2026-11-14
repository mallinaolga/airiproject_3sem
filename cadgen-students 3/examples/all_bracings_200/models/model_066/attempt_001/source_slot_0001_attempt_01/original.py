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
r=extrude(r, (0, 0, 77), 'XY', "sketch().push([(-62.5, -15)]).rect(35, 22).finalize()", -153)
r=extrude(r, (-63, -15, 4), 'XY', "sketch().push([(-63, -15)]).rect(58, 36).finalize()", -30, False)
r=extrude(r, (-91, 0, 0), 'ZX', "sketch().segment((-87, -91), (-2, -89)).arc((-3, -87), (-2, -85)).arc((0, -84), (2, -85)).arc((3, -87), (2, -89)).segment((87, -91)).close().assemble().finalize()", 19)
r=extrude(r, (-43, -20, 67), 'YZ', "sketch().push([(-20, 67)]).circle(3).finalize()", 8)
r=extrude(r, (-77, -12, -63), 'YZ', "sketch().push([(-12, -63)]).rect(130, 30).finalize()", -23)
r=extrude(r, (-77, -7, -45), 'YZ', "sketch().segment((-8, -46), (-8, -44)).segment((-7, -44)).segment((-6, -44)).segment((-6, -46)).close().assemble().finalize()", -19)
r=extrude(r, (-77, 43, -54), 'XY', "sketch().push([(13, 43)]).rect(180, 68).finalize()", 70)
r=extrude(r, (80, 33, 15), 'ZX', "sketch().segment((15, 60), (15, 100)).segment((30, 94)).arc((44, 100), (58, 94)).arc((64, 80), (58, 66)).arc((44, 60), (30, 66)).close().assemble().finalize()", 17)
