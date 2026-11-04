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
r=extrude(r, (0, -101, 0), 'ZX', "sketch().push([(0, -7)]).circle(21).finalize()", 215)
r=extrude(r, (-7, 51, 0), 'ZX', "sketch().push([(0, -7)]).circle(32).finalize()", 29, False)
r=extrude(r, (-22, -101, 11), 'ZX', "sketch().push([(11, -22)]).rect(8, 14).finalize()", -2)
r=extrude(r, (-27, 98, 0), 'YZ', "sketch().push([(98, 0)]).rect(2, 2).finalize()", -2)
r=extrude(r, (-12, -101, -10), 'ZX', "sketch().push([(-10, -12)]).rect(14, 12).push([(-10, -12)]).circle(2, mode='s').finalize()", -14)
r=extrude(r, (14, -38, 0), 'ZX', "sketch().segment((-10, 11), (-10, 39)).segment((10, 39)).segment((10, 11)).arc((0, 14), (-10, 11)).assemble().finalize()", -9)
