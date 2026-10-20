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
r=extrude(r, (0, -21, 0), 'ZX', "sketch().push([(12, 21.5)]).rect(134, 157).finalize()", 6)
r=extrude(r, (-19, -16, -33), 'ZX', "sketch().segment((-79, 62), (13, -13)).segment((-59, -100)).arc((-55, -17), (-79, 62)).assemble().finalize()", 37)
