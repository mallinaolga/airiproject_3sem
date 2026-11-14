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
r=extrude(r, (0, -79, 0), 'ZX', "sketch().push([(-24, 30)]).circle(6).finalize()", 107)
r=extrude(r, (30, -18, -24), 'ZX', "sketch().push([(-24, 30)]).circle(7).finalize()", 15, False)
r=extrude(r, (30, 20, -18), 'XY', "sketch().push([(30, 20)]).rect(66, 44).finalize()", 20)
r=extrude(r, (47, 34, 2), 'XY', "sketch().push([(47, 34)]).rect(56, 90).finalize()", 35)
r=extrude(r, (-4, 24, -15), 'YZ', "sketch().push([(24, -15)]).rect(2, 2).finalize()", -66)
r=extrude(r, (69, 15, 37), 'XY', "sketch().push([(69, 15)]).rect(4, 4).push([(69, 15)]).circle(1, mode='s').finalize()", 23)
r=extrude(r, (-68, 22, -15), 'XY', "sketch().segment((-100, 22), (-36, 22)).segment((-45, -4)).arc((-36, -27), (-45, -50)).arc((-68, -59), (-91, -50)).arc((-100, -27), (-91, -4)).close().assemble().finalize()", 10)
r=extrude(r, (31, -18, -31), 'YZ', "sketch().segment((-79, -60), (-79, -2)).segment((-26, -2)).segment((-18, -2)).segment((-18, -60)).segment((-26, -60)).close().assemble().push([(-52, -31)]).circle(24, mode='s').finalize()", 69)
