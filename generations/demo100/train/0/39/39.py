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
r=extrude(r, (-25, 0, 0), 'YZ', "sketch().push([(9, -68)]).circle(24).finalize()", -59)
r=extrude(r, (-84, -6, -74), 'YZ', "sketch().push([(-6, -74)]).circle(26).push([(-6, -74)]).circle(22, mode='s').finalize()", -16)
r=extrude(r, (-88, -6, -52), 'YZ', "sketch().segment((-20, -59), (-20, 100)).segment((8, 100)).segment((8, -59)).arc((-6, -52), (-20, -59)).assemble().finalize()", 188)
