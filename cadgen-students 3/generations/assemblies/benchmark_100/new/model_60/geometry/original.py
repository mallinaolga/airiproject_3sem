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
r=extrude(r, (0, -101, 0), 'ZX', "sketch().push([(26, 7)]).circle(12).finalize()", 210)
r=extrude(r, (7, -4, 26), 'ZX', "sketch().push([(26, 7)]).circle(20).finalize()", 31, False)
r=extrude(r, (-8, -4, 18), 'ZX', "sketch().push([(18, -8)]).circle(2).finalize()", -34)
r=extrude(r, (7, -58, 14), 'ZX', "sketch().segment((-47, 2), (-47, 12)).segment((15, 12)).arc((14, 7), (15, 2)).close().assemble().finalize()", -2)
r=extrude(r, (7, -101, 38), 'YZ', "sketch().arc((-108, 36), (-109, 38), (-108, 40)).arc((-105, 41), (-103, 40)).segment((-101, 41)).segment((-101, 35)).segment((-103, 36)).arc((-105, 35), (-108, 36)).assemble().finalize()", -34)
