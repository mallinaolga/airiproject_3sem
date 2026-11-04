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
r=extrude(r, (0, 0, -99), 'XY', "sketch().push([(7.5, -3)]).rect(19, 26).finalize()", 178)
r=extrude(r, (8, -3, 66), 'XY', "sketch().push([(8, -3)]).rect(30, 38).finalize()", 40, False)
r=extrude(r, (-2, -4, -61), 'YZ', "sketch().push([(-4, -61)]).circle(4).finalize()", -14)
r=extrude(r, (4, 10, -21), 'YZ', "sketch().push([(4, -21)]).rect(12, 196).finalize()", 2)
r=extrude(r, (-3, -22, 96), 'ZX', "sketch().push([(96, -3)]).rect(2, 8).finalize()", -1)
r=extrude(r, (4, 10, 29), 'ZX', "sketch().push([(29, 4)]).circle(3).finalize()", 23)
r=extrude(r, (-2, -22, 99), 'ZX', "sketch().push([(99, -2)]).circle(20).finalize()", -10)
