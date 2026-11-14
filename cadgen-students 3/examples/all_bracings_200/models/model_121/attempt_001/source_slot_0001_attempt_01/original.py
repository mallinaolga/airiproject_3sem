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
r=extrude(r, (0, -37, 0), 'ZX', "sketch().push([(-25, 38)]).circle(7).finalize()", 127)
r=extrude(r, (38, -15, -25), 'ZX', "sketch().push([(-25, 38)]).circle(10).finalize()", 15, False)
r=extrude(r, (44, -31, -25), 'YZ', "sketch().segment((-91, -40), (-65, 4)).segment((-73, 29)).segment((-26, 43)).segment((-19, 19)).segment((29, -10)).segment((3, -54)).segment((11, -79)).segment((-36, -93)).segment((-43, -69)).close().assemble().finalize()", 72)
r=extrude(r, (44, -31, 2), 'ZX', "sketch().push([(2, -23.5)]).rect(190, 135).finalize()", -41)
r=extrude(r, (-86, -31, -83), 'ZX', "sketch().push([(-83, -86)]).circle(14).push([(-83, -86)]).circle(12, mode='s').finalize()", 55)
r=extrude(r, (-86, 10, -69), 'XY', "sketch().push([(-86, 10)]).circle(31).finalize()", 50)
