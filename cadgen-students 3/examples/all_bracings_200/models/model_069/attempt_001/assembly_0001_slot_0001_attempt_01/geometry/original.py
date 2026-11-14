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
r=extrude(r, (-94, 0, 0), 'YZ', "sketch().push([(-4, -0.5)]).rect(44, 39).finalize()", 174)
r=extrude(r, (-75, -4, -1), 'YZ', "sketch().push([(-4, -1)]).rect(72, 64).finalize()", 24, False)
r=extrude(r, (-94, 11, -20), 'YZ', "sketch().push([(11, 6.5)]).rect(58, 53).finalize()", 16)
r=extrude(r, (59, 5, 19), 'XY', "sketch().push([(59, 5)]).rect(70, 58).push([(59, 5)]).circle(18, mode='s').finalize()", 11)
r=extrude(r, (9, 16, 19), 'YZ', "sketch().push([(16, 6.5)]).rect(36, 25).finalize()", -54)
r=extrude(r, (5, -7, 19), 'XY', "sketch().push([(5, -7)]).circle(2).finalize()", 9)
r=extrude(r, (4, -16, -20), 'XY', "sketch().push([(4, -16)]).circle(19).finalize()", -14)
