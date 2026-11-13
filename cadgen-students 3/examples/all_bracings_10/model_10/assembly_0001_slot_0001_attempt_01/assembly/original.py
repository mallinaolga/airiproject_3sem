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
r=extrude(r, (0, 0, -96), 'XY', "sketch().push([(-3.5, 0)]).rect(29, 30).finalize()", 193)
r=extrude(r, (-4, 0, -80), 'XY', "sketch().push([(-4, 0)]).rect(48, 48).finalize()", 31, False)
r=extrude(r, (-17, 24, -60), 'YZ', "sketch().push([(23.5, -60)]).rect(1, 6).finalize()", 45)
r=extrude(r, (-15, -14, -93), 'ZX', "sketch().push([(-93, -15)]).circle(2).finalize()", -2)
r=extrude(r, (-3, -14, 36), 'ZX', "sketch().segment((34, 2), (34, 14)).segment((37, 14)).segment((37, 2)).arc((37, -20), (34, 2)).assemble().finalize()", -7)
