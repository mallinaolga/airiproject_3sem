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
r=extrude(r, (0, 0, -29), 'XY', "sketch().push([(-23, 0)]).circle(3).finalize()", 115)
r=extrude(r, (-20, 0, 0), 'YZ', "sketch().segment((-85, -100), (-85, 34)).segment((27, 34)).arc((54, 99), (59, 29)).segment((59, 22)).segment((20, 22)).segment((20, -100)).close().assemble().push([(-27, 12)]).circle(10, mode='s').finalize()", 46)
