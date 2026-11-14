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
r=extrude(r, (0, 0, -24), 'XY', "sketch().push([(21, -24)]).circle(9).finalize()", 97)
r=extrude(r, (21, -24, -1), 'XY', "sketch().push([(21, -24)]).circle(13).finalize()", 37, False)
r=extrude(r, (15, -13, -2), 'XY', "sketch().push([(15, -13)]).rect(2, 2).finalize()", -60)
r=extrude(r, (21, -11, 32), 'ZX', "sketch().push([(32, 21)]).circle(80).finalize()", 47)
r=extrude(r, (14, -13, -26), 'YZ', "sketch().push([(-13, -26)]).rect(2, 8).finalize()", -114)
r=extrude(r, (16, -14, -62), 'XY', "sketch().segment((15, -14), (16, -13)).segment((17, -14)).segment((16, -15)).close().assemble().finalize()", -51)
