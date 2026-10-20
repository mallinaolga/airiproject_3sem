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
r=extrude(r, (-100, 0, 0), 'YZ', "sketch().segment((-72, -87), (-72, -13)).segment((-44, -13)).arc((-29, -2), (-14, -13)).segment((-5, -13)).segment((16, 87)).segment((28, 85)).segment((7, -13)).segment((72, -13)).segment((72, -87)).close().assemble().finalize()", 200)
