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
r=extrude(r, (109, 0, 0), 'YZ', "sketch().push([(9, 0)]).rect(28, 28).finalize()", -217)
r=extrude(r, (98, 9, 0), 'YZ', "sketch().push([(9, 0)]).rect(46, 48).finalize()", -36, False)
r=extrude(r, (8, -3, 14), 'XY', "sketch().push([(8, -3)]).circle(29).finalize()", 3)
r=extrude(r, (98, 10, 18), 'YZ', "sketch().push([(10, 18)]).circle(4).push([(10, 18)]).circle(3, mode='s').finalize()", 9)
