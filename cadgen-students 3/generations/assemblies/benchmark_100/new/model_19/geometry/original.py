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
r=extrude(r, (0, 0, -99), 'XY', "sketch().push([(-1, -3.5)]).rect(16, 25).finalize()", 197)
r=extrude(r, (-1, -4, -37), 'XY', "sketch().push([(-1, -4)]).rect(26, 38).finalize()", 83, False)
r=extrude(r, (1, -23, 40), 'ZX', "sketch().push([(40, 1)]).rect(8, 6).finalize()", -6)
r=extrude(r, (12, -17, -22), 'YZ', "sketch().push([(-17, -22)]).circle(4).finalize()", 12)
r=extrude(r, (0, 9, 80), 'ZX', "sketch().push([(80, 0)]).rect(38, 62).finalize()", 20)
