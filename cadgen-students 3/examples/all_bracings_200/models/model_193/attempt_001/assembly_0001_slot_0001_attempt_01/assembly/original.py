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
r=extrude(r, (0, 94, 0), 'ZX', "sketch().push([(0, -2)]).circle(14).finalize()", -190)
r=extrude(r, (-2, 9, 0), 'ZX', "sketch().push([(0, -2)]).circle(23).finalize()", -77, False)
r=extrude(r, (12, 9, 17), 'ZX', "sketch().push([(17, 12)]).rect(2, 4).finalize()", 59)
r=extrude(r, (8, 94, -4), 'ZX', "sketch().segment((-6, 10), (-3, 11)).segment((-2, 8)).segment((-4, 7)).arc((-5, 5), (-5, 7)).close().assemble().finalize()", 2)
r=extrude(r, (11, 18, 0), 'YZ', "sketch().push([(18, 0)]).rect(2, 4).finalize()", 14)
