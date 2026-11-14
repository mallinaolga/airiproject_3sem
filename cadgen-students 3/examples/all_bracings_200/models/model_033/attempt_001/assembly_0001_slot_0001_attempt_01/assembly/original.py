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
r=extrude(r, (0, 65, 0), 'ZX', "sketch().push([(26, 0)]).circle(29).finalize()", -176)
r=extrude(r, (0, 38, 26), 'ZX', "sketch().push([(26, 0)]).circle(33).finalize()", -45, False)
r=extrude(r, (0, 64, 54), 'ZX', "sketch().arc((49, -15), (54, 0), (49, 15)).segment((55, 15)).segment((55, -15)).close().assemble().finalize()", 47)
r=extrude(r, (0, 21, -7), 'XY', "sketch().push([(0, 21)]).rect(34, 36).finalize()", -5)
r=extrude(r, (6, 12, -13), 'XY', "sketch().segment((2, 13), (8, 16)).segment((10, 11)).segment((4, 8)).close().assemble().finalize()", -46)
