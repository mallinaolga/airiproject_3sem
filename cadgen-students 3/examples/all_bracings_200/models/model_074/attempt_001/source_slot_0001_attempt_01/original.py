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
r=extrude(r, (94, 0, 0), 'YZ', "sketch().push([(0, -34)]).rect(82, 14).finalize()", -189)
r=extrude(r, (-52, 0, -34), 'YZ', "sketch().push([(0, -34)]).rect(96, 16).finalize()", -19, False)
r=extrude(r, (-64, -33, -26), 'XY', "sketch().segment((-66, -33), (-63, -31)).segment((-62, -33)).segment((-65, -35)).close().assemble().finalize()", 39)
r=extrude(r, (14, -9, -27), 'XY', "sketch().push([(14, -9)]).circle(28).finalize()", 13)
r=extrude(r, (-50, 4, -41), 'YZ', "sketch().segment((-28, -41), (-19, -23)).arc((-28, 0), (-19, 22)).arc((4, 32), (27, 22)).arc((36, 0), (27, -23)).segment((36, -41)).close().assemble().finalize()", 39)
r=extrude(r, (-44, 4, 32), 'YZ', "sketch().segment((-22, 17), (-22, 41)).segment((30, 41)).segment((30, 17)).arc((4, 32), (-22, 17)).assemble().finalize()", 118)
r=extrude(r, (28, 11, -15), 'XY', "sketch().push([(28, 11)]).circle(1).finalize()", 18)
