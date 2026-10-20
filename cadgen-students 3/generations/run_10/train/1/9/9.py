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
r=extrude(r, (0, -24, 0), 'ZX', "sketch().arc((-8, 51), (-10, 77), (4, 100)).arc((2, 42), (58, 25)).arc((-28, -94), (-8, 51)).assemble().finalize()", -46)
r=extrude(r, (-40, -24, -58), 'ZX', "sketch().push([(-58, -40)]).circle(7).finalize()", 95)
