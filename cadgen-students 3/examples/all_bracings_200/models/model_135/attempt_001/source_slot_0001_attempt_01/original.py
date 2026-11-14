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
r=extrude(r, (0, -120, 0), 'ZX', "sketch().push([(7, -20)]).rect(42, 40).finalize()", 199)
r=extrude(r, (-20, 63, 7), 'ZX', "sketch().push([(7, -20)]).rect(66, 62).finalize()", 56, False)
r=extrude(r, (-2, 50, -14), 'XY', "sketch().push([(-2, 50)]).circle(1).finalize()", -26)
r=extrude(r, (-51, 78, -19), 'YZ', "sketch().push([(78, -19)]).rect(4, 6).push([(78, -19)]).circle(1, mode='s').finalize()", -6)
r=extrude(r, (-40, -22, 26), 'YZ', "sketch().push([(-22, 26)]).circle(2).finalize()", -18)
r=extrude(r, (0, 55, 8), 'YZ', "sketch().segment((51, 8), (55, 12)).segment((59, 8)).segment((55, 4)).close().assemble().finalize()", 11)
r=extrude(r, (0, 50, 23), 'YZ', "sketch().push([(50, 23)]).circle(2).finalize()", 58)
