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
r=extrude(r, (-86, 0, 0), 'YZ', "sketch().push([(-14, -2)]).circle(13).finalize()", 202)
r=extrude(r, (-44, -14, -2), 'YZ', "sketch().push([(-14, -2)]).circle(22).finalize()", 46, False)
r=extrude(r, (-78, -2, -2), 'YZ', "sketch().arc((-6, -10), (-2, -2), (-6, 6)).segment((8, 4)).arc((14, 6), (19, 4)).arc((22, -2), (19, -8)).arc((14, -10), (8, -8)).close().assemble().finalize()", -17)
r=extrude(r, (-95, 5, 0), 'YZ', "sketch().push([(5, 0)]).rect(2, 4).finalize()", -20)
r=extrude(r, (-78, 21, 0), 'ZX', "sketch().segment((-25, -78), (25, -78)).segment((12, -87)).arc((17, -99), (12, -111)).arc((0, -116), (-12, -111)).arc((-17, -99), (-12, -87)).close().assemble().finalize()", 16)
