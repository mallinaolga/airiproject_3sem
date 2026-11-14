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
r=extrude(r, (0, 0, -66), 'XY', "sketch().push([(-62, 0)]).circle(43).finalize()", 156)
r=extrude(r, (-62, 0, -56), 'XY', "sketch().push([(-62, 0)]).circle(51).finalize()", 34, False)
r=extrude(r, (-10, 0, -52), 'XY', "sketch().arc((-13, -15), (-10, 0), (-13, 15)).segment((113, 15)).segment((113, -15)).close().assemble().finalize()", 26)
r=extrude(r, (67, -15, -51), 'YZ', "sketch().push([(-26, -51)]).rect(22, 78).finalize()", 16)
r=extrude(r, (58, -9, -27), 'XY', "sketch().push([(58, -9)]).rect(10, 62).finalize()", 21)
r=extrude(r, (10, -2, -27), 'XY', "sketch().push([(10, -2)]).rect(6, 2).finalize()", 11)
