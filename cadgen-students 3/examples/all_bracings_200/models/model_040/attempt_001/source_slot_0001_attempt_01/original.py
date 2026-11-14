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
r=extrude(r, (0, 0, -60), 'XY', "sketch().push([(-5, -23)]).circle(4).finalize()", 33)
r=extrude(r, (-5, -23, -35), 'XY', "sketch().push([(-5, -23)]).circle(6).finalize()", 3, False)
r=extrude(r, (-5, -19, -57), 'ZX', "sketch().push([(-57, -5)]).rect(94, 120).finalize()", 92)
r=extrude(r, (-65, 6, -21), 'YZ', "sketch().push([(6, -21)]).circle(9).finalize()", -24)
r=extrude(r, (21, -4, -10), 'XY', "sketch().push([(21, -4)]).rect(136, 218).finalize()", 110)
r=extrude(r, (-33, 106, 46), 'ZX', "sketch().push([(46, -33)]).rect(116, 48).finalize()", 7)
