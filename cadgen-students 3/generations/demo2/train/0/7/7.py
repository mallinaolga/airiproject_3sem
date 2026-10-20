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
r=extrude(r, (0, 0, -67), 'XY', "sketch().segment((-88, -88), (-88, 4)).segment((34, 4)).segment((34, 100)).segment((66, 100)).segment((66, 4)).segment((88, 4)).segment((88, -88)).segment((66, -88)).segment((66, -100)).segment((34, -100)).segment((34, -88)).close().assemble().finalize()", 134)
