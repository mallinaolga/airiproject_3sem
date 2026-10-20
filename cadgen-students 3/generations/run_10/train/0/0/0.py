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
r=extrude(r, (0, 21, 0), 'ZX', "sketch().push([(17, 10)]).circle(78).push([(0, 0)]).circle(74, mode='s').finalize()", -84)
r=extrude(r, (27, 21, 0), 'YZ', "sketch().segment((21, -100), (21, 100)).segment((41, 100)).segment((41, -39)).segment((64, -39)).segment((64, -99)).segment((41, -99)).segment((41, -100)).close().assemble().finalize()", -115)
