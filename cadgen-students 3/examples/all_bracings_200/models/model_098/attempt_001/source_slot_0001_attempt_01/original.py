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
r=extrude(r, (0, 0, 105), 'XY', "sketch().push([(0, 0.5)]).rect(36, 3).finalize()", -192)
r=extrude(r, (0, 0, -82), 'XY', "sketch().push([(0, 0)]).rect(44, 4).finalize()", -22, False)
r=extrude(r, (-5, 4, 91), 'ZX', "sketch().push([(91, -5)]).circle(9).finalize()", 16)
r=extrude(r, (-15, 1, 21), 'XY', "sketch().push([(-15, -10)]).rect(4, 22).finalize()", 12)
r=extrude(r, (-5, 1, 49), 'ZX', "sketch().push([(49, -5)]).circle(4).finalize()", -18)
r=extrude(r, (0, 1, 95), 'ZX', "sketch().segment((91, 3), (98, 4)).segment((99, -3)).segment((92, -4)).close().assemble().finalize()", -20)
