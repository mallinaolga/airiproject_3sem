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
r=extrude(r, (0, 7, 0), 'ZX', "sketch().push([(6, -11)]).circle(26).finalize()", 89)
r=extrude(r, (-11, 20, 6), 'ZX', "sketch().push([(6, -11)]).circle(31).finalize()", 12, False)
r=extrude(r, (-37, 70, 6), 'YZ', "sketch().push([(70, 6)]).rect(36, 128).finalize()", -33)
r=extrude(r, (-33, 7, 6), 'YZ', "sketch().push([(-46.5, 6)]).rect(107, 94).finalize()", 12)
r=extrude(r, (-37, 69, 51), 'YZ', "sketch().push([(69, 51)]).circle(9).finalize()", 47)
r=extrude(r, (6, 96, 0), 'ZX', "sketch().push([(0, 6)]).rect(178, 128).finalize()", 4)
