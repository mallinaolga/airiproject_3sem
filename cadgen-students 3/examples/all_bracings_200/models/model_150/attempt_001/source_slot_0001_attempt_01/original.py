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
r=extrude(r, (30, 0, 0), 'YZ', "sketch().push([(-10, -2)]).circle(13).finalize()", -132)
r=extrude(r, (-12, -10, -2), 'YZ', "sketch().push([(-10, -2)]).circle(17).finalize()", -20, False)
r=extrude(r, (-28, -10, 15), 'YZ', "sketch().segment((-22, 9), (-19, 25)).arc((-22, 34), (-19, 42)).arc((-10, 46), (-1, 42)).arc((2, 34), (-1, 25)).segment((2, 9)).arc((-10, 15), (-22, 9)).assemble().push([(-10, 34)]).circle(6, mode='s').finalize()", 74)
r=extrude(r, (-25, 7, -2), 'ZX', "sketch().push([(-2, -25)]).circle(1).finalize()", 48)
r=extrude(r, (30, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(61).finalize()", 72)
r=extrude(r, (-67, -24, -2), 'ZX', "sketch().push([(-2, -67)]).rect(6, 6).finalize()", -23)
