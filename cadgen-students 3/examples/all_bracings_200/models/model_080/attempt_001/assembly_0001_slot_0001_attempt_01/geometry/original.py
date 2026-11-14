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
r=extrude(r, (0, -67, 0), 'ZX', "sketch().push([(-95.5, 1)]).rect(17, 14).finalize()", 118)
r=extrude(r, (1, -10, -96), 'ZX', "sketch().push([(-96, 1)]).rect(28, 22).finalize()", 22, False)
r=extrude(r, (-3, 4, -81), 'XY', "sketch().push([(-3, 4)]).circle(2).push([(-3, 4)]).circle(1, mode='s').finalize()", 64)
r=extrude(r, (-3, 5, -21), 'ZX', "sketch().push([(-21, -3)]).circle(85).finalize()", 62)
r=extrude(r, (0, -49, -84), 'XY', "sketch().push([(0, -49)]).rect(210, 36).finalize()", 197)
