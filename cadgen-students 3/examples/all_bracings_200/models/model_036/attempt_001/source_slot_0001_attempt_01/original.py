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
r=extrude(r, (0, 46, 0), 'ZX', "sketch().push([(81, 6)]).circle(3).finalize()", 59)
r=extrude(r, (6, 91, 81), 'ZX', "sketch().push([(81, 6)]).circle(4).finalize()", 16, False)
r=extrude(r, (6, 89, 85), 'XY', "sketch().push([(6, 89)]).rect(18, 16).finalize()", 8)
r=extrude(r, (14, 81, 86), 'YZ', "sketch().push([(-10, 86)]).rect(182, 46).finalize()", -55)
r=extrude(r, (14, -41, 78), 'YZ', "sketch().segment((-68, 97), (-50, 109)).segment((-35, 89)).arc((-31, 85), (-29, 80)).segment((-14, 59)).segment((-32, 47)).segment((-47, 67)).arc((-51, 71), (-53, 76)).close().assemble().finalize()", 28)
r=extrude(r, (-30, 0, 63), 'XY', "sketch().push([(-30, 0)]).rect(18, 214).finalize()", -94)
r=extrude(r, (-15, 30, 63), 'XY', "sketch().push([(-15, 30)]).rect(8, 18).finalize()", -172)
