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
r=extrude(r, (0, 0, 20), 'XY', "sketch().push([(0, 0)]).rect(200, 198).push([(0, 0)]).circle(30, mode='s').push([(-51, 28)]).circle(10, mode='s').finalize()", -55)
r=extrude(r, (-69, -5, 20), 'XY', "sketch().segment((-75, -22), (-75, -13)).arc((-82, -4), (-75, 5)).segment((-75, 12)).segment((-56, 12)).segment((-56, -22)).close().assemble().finalize()", 16)
