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
r=extrude(r, (0, 0, 80), 'XY', "sketch().push([(-2.5, 3)]).rect(31, 42).finalize()", -154)
r=extrude(r, (-2, 3, -68), 'XY', "sketch().push([(-2, 3)]).rect(42, 56).finalize()", -42, False)
r=extrude(r, (13, -7, 80), 'ZX', "sketch().arc((62, 7), (59, 13), (62, 19)).arc((68, 21), (74, 19)).segment((80, 21)).segment((80, 5)).segment((74, 7)).arc((68, 5), (62, 7)).assemble().finalize()", 6)
r=extrude(r, (13, -16, -27), 'YZ', "sketch().push([(-16, -27)]).circle(1).finalize()", 10)
r=extrude(r, (-18, -7, 24), 'YZ', "sketch().push([(-7, 24)]).rect(48, 12).finalize()", -5)
r=extrude(r, (-13, 8, 80), 'XY', "sketch().push([(-13, 8)]).circle(2).finalize()", 31)
