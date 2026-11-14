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
r=extrude(r, (0, 70, 0), 'ZX', "sketch().push([(-4.5, -23)]).rect(17, 6).finalize()", -162)
r=extrude(r, (-23, -38, -5), 'ZX', "sketch().push([(-5, -23)]).rect(26, 10).finalize()", -54, False)
r=extrude(r, (-21, 54, 4), 'XY', "sketch().push([(-21, 54)]).circle(1).finalize()", 15)
r=extrude(r, (-18, -68, -8), 'YZ', "sketch().push([(-68, -8)]).circle(11).finalize()", 39)
r=extrude(r, (11, -57, -8), 'YZ', "sketch().arc((-62, -16), (-57, -8), (-62, 0)).segment((92, 0)).segment((92, -16)).close().assemble().finalize()", 17)
