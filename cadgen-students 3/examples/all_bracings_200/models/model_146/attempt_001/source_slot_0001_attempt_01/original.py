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
r=extrude(r, (-80, 0, 0), 'YZ', "sketch().push([(0, -1)]).circle(13).finalize()", 173)
r=extrude(r, (-7, 0, -1), 'YZ', "sketch().push([(0, -1)]).circle(17).finalize()", 20, False)
r=extrude(r, (-66, 13, -1), 'ZX', "sketch().push([(-1, -66)]).rect(4, 14).finalize()", 1)
r=extrude(r, (-7, 16, 5), 'YZ', "sketch().push([(16, 5)]).circle(1).finalize()", -40)
r=extrude(r, (-80, 0, -11), 'XY', "sketch().arc((-92, -4), (-94, 0), (-92, 4)).arc((-88, 6), (-83, 4)).segment((-80, 21)).segment((-80, -21)).segment((-83, -4)).arc((-88, -6), (-92, -4)).assemble().finalize()", 11)
r=extrude(r, (-43, 0, 11), 'XY', "sketch().push([(-43, 0)]).rect(2, 2).finalize()", 7)
