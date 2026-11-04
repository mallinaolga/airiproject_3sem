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
r=extrude(r, (0, -107, 0), 'ZX', "sketch().push([(0, -24)]).circle(12).finalize()", 202)
r=extrude(r, (-24, 66, 0), 'ZX', "sketch().push([(0, -24)]).circle(20).finalize()", 40, False)
r=extrude(r, (-5, 91, 0), 'ZX', "sketch().segment((-8, -7), (-8, 42)).segment((8, 42)).segment((8, -7)).arc((0, -5), (-8, -7)).assemble().finalize()", -172)
r=extrude(r, (42, 52, 5), 'YZ', "sketch().push([(52, 5)]).rect(76, 20).finalize()", 2)
