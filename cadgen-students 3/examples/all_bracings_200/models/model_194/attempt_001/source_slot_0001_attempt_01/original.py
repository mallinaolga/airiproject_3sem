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
r=extrude(r, (-35, 0, 0), 'YZ', "sketch().push([(-40, 0)]).circle(4).finalize()", 34)
r=extrude(r, (-16, -40, 0), 'YZ', "sketch().push([(-40, 0)]).circle(6).finalize()", 9, False)
r=extrude(r, (-21, -40, -4), 'XY', "sketch().push([(-21, -40)]).rect(78, 6).finalize()", -53)
r=extrude(r, (-3, -36, 0), 'ZX', "sketch().segment((-74, -11), (-36, 19)).segment((-55, 58)).segment((-11, 78)).segment((3, 49)).segment((17, 60)).segment((74, -13)).segment((-17, -84)).close().assemble().finalize()", 48)
r=extrude(r, (8, 11, 2), 'ZX', "sketch().segment((-55, -77), (-55, 93)).segment((-39, 93)).segment((-39, 78)).segment((59, 78)).segment((59, -77)).close().assemble().finalize()", 6)
r=extrude(r, (0, 18, -8), 'ZX', "sketch().push([(-8, 0)]).rect(82, 202).push([(-8, 0)]).circle(37, mode='s').finalize()", 16)
r=extrude(r, (-68, 34, -8), 'ZX', "sketch().push([(-8, -68)]).circle(24).finalize()", 12)
