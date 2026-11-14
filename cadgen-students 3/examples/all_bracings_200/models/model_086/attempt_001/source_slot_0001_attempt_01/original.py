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
r=extrude(r, (0, 112, 0), 'ZX', "sketch().push([(15, -24)]).circle(14).finalize()", -224)
r=extrude(r, (-24, 40, 15), 'ZX', "sketch().push([(15, -24)]).circle(19).finalize()", -33, False)
r=extrude(r, (-10, -27, 15), 'YZ', "sketch().push([(-27, 15)]).circle(12).finalize()", 26)
r=extrude(r, (-24, -69, 30), 'XY', "sketch().push([(-24, -69)]).circle(6).finalize()", 3)
r=extrude(r, (0, -15, 15), 'YZ', "sketch().arc((-17, 10), (-15, 15), (-17, 20)).segment((0, 19)).arc((3, 20), (7, 19)).arc((8, 15), (7, 11)).arc((3, 10), (0, 11)).close().assemble().finalize()", 43)
r=extrude(r, (13, 4, 10), 'XY', "sketch().push([(13, 4)]).circle(28).finalize()", -44)
