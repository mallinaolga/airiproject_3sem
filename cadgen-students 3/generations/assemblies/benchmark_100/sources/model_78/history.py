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
r=extrude(r, (106, 0, 0), 'YZ', "sketch().push([(-23, 25)]).circle(11).finalize()", -213)
r=extrude(r, (6, -23, 25), 'YZ', "sketch().push([(-23, 25)]).circle(14).finalize()", -85, False)
r=extrude(r, (-44, -23, 11), 'YZ', "sketch().arc((-33, 16), (-23, 11), (-13, 16)).segment((-16, -6)).arc((-13, -13), (-16, -20)).arc((-23, -23), (-30, -20)).arc((-33, -13), (-30, -6)).close().assemble().finalize()", 60)
r=extrude(r, (-23, -13, -13), 'ZX', "sketch().arc((-32, -41), (3, -2), (-26, -46)).segment((-17, -46)).segment((-17, -36)).segment((-32, -36)).close().assemble().finalize()", 15)
r=extrude(r, (-10, 2, -29), 'ZX', "sketch().push([(-29, -10)]).circle(1).finalize()", 35)
