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
r=extrude(r, (-96, 0, 0), 'YZ', "sketch().push([(-8, -4.5)]).rect(24, 9).finalize()", 171)
r=extrude(r, (75, -8, -4), 'YZ', "sketch().push([(-8, -4)]).rect(32, 12).finalize()", 21, False)
r=extrude(r, (-63, 2, 0), 'XY', "sketch().push([(-63, 2)]).circle(1).finalize()", 13)
r=extrude(r, (-51, 0, -9), 'XY', "sketch().push([(-51, 0)]).rect(44, 54).finalize()", -4)
r=extrude(r, (84, -4, -11), 'XY', "sketch().segment((80, -5), (80, -1)).segment((85, -1)).segment((85, -3)).arc((88, -6), (83, -5)).close().assemble().finalize()", -2)
