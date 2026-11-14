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
r=extrude(r, (0, -89, 0), 'ZX', "sketch().push([(0, -8)]).circle(15).finalize()", 198)
r=extrude(r, (-8, 39, 0), 'ZX', "sketch().push([(0, -8)]).circle(19).finalize()", 24, False)
r=extrude(r, (6, -17, 0), 'YZ', "sketch().push([(-17, 0)]).circle(51).finalize()", 19)
r=extrude(r, (0, -89, 1), 'ZX', "sketch().push([(1, 0)]).circle(28).finalize()", -20)
