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
r=extrude(r, (0, 115, 0), 'ZX', "sketch().push([(-14, 7)]).circle(24).finalize()", -233)
r=extrude(r, (7, 14, -14), 'ZX', "sketch().push([(-14, 7)]).circle(30).finalize()", -31, False)
r=extrude(r, (31, -39, -14), 'YZ', "sketch().push([(-39, -14)]).rect(22, 24).push([(-41, -12)]).circle(5, mode='s').finalize()", 7)
r=extrude(r, (7, -51, 10), 'XY', "sketch().push([(7, -51)]).rect(46, 24).finalize()", 33)
r=extrude(r, (-3, 115, -7), 'ZX', "sketch().push([(-7, -3)]).rect(40, 68).finalize()", 4)
