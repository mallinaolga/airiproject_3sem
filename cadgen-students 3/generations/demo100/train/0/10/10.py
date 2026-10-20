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
r=extrude(r, (20, 0, 0), 'YZ', "sketch().segment((-100, 39), (-85, 44)).arc((-48, 83), (7, 79)).segment((21, 84)).segment((38, 38)).arc((73, 30), (90, -1)).segment((100, -3)).segment((97, -25)).segment((87, -23)).arc((49, -52), (7, -31)).arc((-25, -40), (-57, -31)).segment((-72, -37)).close().assemble().finalize()", -23)
r=extrude(r, (-2, -25, -40), 'XY', "sketch().push([(-2, -25)]).circle(18).finalize()", -47)
