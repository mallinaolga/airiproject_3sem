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
r=extrude(r, (-94, 0, 0), 'YZ', "sketch().push([(-7, -8.5)]).rect(64, 47).finalize()", 189)
r=extrude(r, (-78, -7, -8), 'YZ', "sketch().push([(-7, -8)]).rect(104, 76).finalize()", 19, False)
r=extrude(r, (19, 0, -32), 'XY', "sketch().push([(19, 0)]).rect(108, 120).finalize()", -6)
r=extrude(r, (57, 19, -38), 'YZ', "sketch().push([(19, 4)]).rect(46, 84).finalize()", -90)
r=extrude(r, (-70, 35, 30), 'XY', "sketch().push([(-70, 35)]).rect(12, 44).finalize()", 16)
r=extrude(r, (5, 42, 45), 'ZX', "sketch().push([(45, 5)]).circle(1).finalize()", 12)
