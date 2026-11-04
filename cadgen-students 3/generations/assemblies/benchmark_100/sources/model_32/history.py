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
r=extrude(r, (-115, 0, 0), 'YZ', "sketch().push([(-7.5, -4.5)]).rect(39, 13).finalize()", 208)
r=extrude(r, (51, -8, -5), 'YZ', "sketch().push([(-8, -5)]).rect(56, 20).finalize()", 65, False)
r=extrude(r, (-21, 12, 0), 'ZX', "sketch().push([(0, -21)]).rect(60, 98).finalize()", 24)
r=extrude(r, (-28, -12, 2), 'XY', "sketch().segment((-26, -10), (-26, -7)).segment((-23, -7)).segment((-23, -14)).segment((-25, -14)).arc((-33, -14), (-26, -10)).assemble().finalize()", 17)
r=extrude(r, (-29, -9, 4), 'XY', "sketch().segment((-33, -11), (-33, -8)).segment((-25, -8)).segment((-25, -11)).arc((-29, -9), (-33, -11)).assemble().finalize()", 10)
