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
r=extrude(r, (0, 0, 80), 'XY', "sketch().push([(0, -5)]).circle(12).finalize()", -170)
r=extrude(r, (0, -5, -23), 'XY', "sketch().push([(0, -5)]).circle(19).finalize()", -73, False)
r=extrude(r, (-5, 2, 80), 'XY', "sketch().push([(-5, 2)]).circle(4).push([(-5, 2)]).circle(2, mode='s').finalize()", 15)
r=extrude(r, (-5, 6, 86), 'ZX', "sketch().segment((81, -7), (90, -1)).segment((91, -3)).segment((82, -9)).close().assemble().finalize()", 18)
