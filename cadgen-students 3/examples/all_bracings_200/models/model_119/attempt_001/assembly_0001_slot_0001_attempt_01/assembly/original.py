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
r=extrude(r, (0, 0, -113), 'XY', "sketch().push([(0, -2)]).circle(17).finalize()", 227)
r=extrude(r, (0, -2, 77), 'XY', "sketch().push([(0, -2)]).circle(27).finalize()", 24, False)
r=extrude(r, (0, -19, -90), 'ZX', "sketch().segment((-92, -6), (-92, -3)).arc((-94, 0), (-92, 3)).segment((-92, 6)).segment((-88, 6)).segment((-88, 3)).arc((-86, 0), (-88, -3)).segment((-88, -6)).close().assemble().finalize()", -1)
r=extrude(r, (0, 25, 85), 'ZX', "sketch().segment((84, 9), (84, 10)).segment((96, 10)).segment((96, 5)).segment((91, 5)).arc((78, -8), (84, 9)).assemble().finalize()", 4)
r=extrude(r, (-17, -2, 43), 'YZ', "sketch().push([(-2, 43)]).circle(2).finalize()", -3)
