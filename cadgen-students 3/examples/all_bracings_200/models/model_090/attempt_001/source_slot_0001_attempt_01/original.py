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
r=extrude(r, (81, 0, 0), 'YZ', "sketch().push([(0, 2)]).circle(15).finalize()", -195)
r=extrude(r, (-55, 0, 2), 'YZ', "sketch().push([(0, 2)]).circle(23).finalize()", -21, False)
r=extrude(r, (-85, 0, -14), 'XY', "sketch().push([(-85, 0)]).rect(8, 6).finalize()", -8)
r=extrude(r, (81, 9, 4), 'XY', "sketch().segment((81, -5), (81, 23)).segment((91, 19)).arc((101, 23), (111, 19)).arc((115, 9), (111, -1)).arc((101, -5), (91, -1)).close().assemble().push([(101, 9)]).circle(2, mode='s').finalize()", -18)
r=extrude(r, (-58, 0, 25), 'XY', "sketch().push([(-58, 0)]).circle(17).finalize()", 6)
r=extrude(r, (85, 13, 4), 'XY', "sketch().push([(85, 13)]).circle(3).finalize()", 14)
r=extrude(r, (-88, 0, -22), 'XY', "sketch().push([(-88, 0)]).rect(2, 6).finalize()", -10)
r=extrude(r, (-41, 0, 28), 'XY', "sketch().arc((-44, -9), (-41, 0), (-44, 9)).segment((41, 9)).segment((41, -9)).close().assemble().finalize()", 4)
