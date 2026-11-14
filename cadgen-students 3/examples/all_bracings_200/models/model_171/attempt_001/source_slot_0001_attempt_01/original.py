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
r=extrude(r, (0, 0, 92), 'XY', "sketch().push([(-2, 5.5)]).rect(30, 29).finalize()", -147)
r=extrude(r, (-2, 5, -21), 'XY', "sketch().push([(-2, 5)]).rect(34, 32).finalize()", -41, False)
r=extrude(r, (12, 20, -4), 'YZ', "sketch().arc((-16, -17), (-21, -4), (-16, 9)).arc((-3, 14), (10, 9)).segment((20, 102)).segment((20, -110)).segment((10, -17)).arc((-3, -22), (-16, -17)).assemble().finalize()", -6)
r=extrude(r, (0, -6, 92), 'ZX', "sketch().push([(100, 0)]).rect(16, 92).finalize()", -1)
r=extrude(r, (-4, -11, -34), 'ZX', "sketch().push([(-34, -4)]).circle(8).finalize()", -6)
r=extrude(r, (-6, -9, -20), 'ZX', "sketch().segment((-22, -8), (-22, -4)).segment((-19, -7)).segment((-18, -6)).segment((-18, -8)).close().assemble().finalize()", -6)
