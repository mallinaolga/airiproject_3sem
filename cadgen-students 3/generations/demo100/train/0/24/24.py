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
r=extrude(r, (0, 0, -100), 'XY', "sketch().arc((-28, -90), (-97, -20), (-28, 49)).arc((-13, 56), (2, 59)).segment((36, 91)).segment((97, 27)).segment((63, -5)).arc((54, -31), (35, -50)).arc((10, -79), (-26, -90)).segment((-27, -91)).close().assemble().push([(-28, -21)]).circle(38, mode='s').finalize()", 200)
