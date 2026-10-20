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
r=extrude(r, (-42, 0, 0), 'YZ', "sketch().push([(81.5, -7.5)]).rect(37, 17).finalize()", 85)
r=extrude(r, (19, 72, -8), 'ZX', "sketch().push([(-9, 19)]).rect(2, 2).finalize()", -142)
r=extrude(r, (20, 65, -6), 'XY', "sketch().push([(20, -17.5)]).rect(2, 165).finalize()", 21)
