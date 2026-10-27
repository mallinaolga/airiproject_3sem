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
r=extrude(r, (0, 9, 0), 'ZX', "sketch().push([(18, -48)]).circle(9).finalize()", 73)
r=extrude(r, (-48, 10, 18), 'ZX', "sketch().push([(18, -48)]).circle(14).finalize()", 9, False)
r=extrude(r, (-42, 9, 7), 'ZX', "sketch().push([(7, -42)]).rect(192, 60).finalize()", -84)
r=extrude(r, (-12, -16, -22), 'ZX', "sketch().segment((-95, -12), (-49, 7)).arc((-60, 34), (-49, 61)).arc((-22, 72), (5, 61)).arc((16, 34), (5, 7)).segment((51, -12)).close().assemble().finalize()", -66)
r=extrude(r, (-40, -40, -88), 'XY', "sketch().push([(-40, -40)]).circle(30).finalize()", -15)
