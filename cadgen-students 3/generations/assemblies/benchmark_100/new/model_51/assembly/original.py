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
r=extrude(r, (0, -112, 0), 'ZX', "sketch().push([(-3, 1.5)]).rect(18, 35).finalize()", 223)
r=extrude(r, (1, -108, -3), 'ZX', "sketch().push([(-3, 1)]).rect(26, 52).finalize()", 69, False)
r=extrude(r, (-16, 8, 0), 'YZ', "sketch().push([(8, 0)]).circle(46).finalize()", -10)
r=extrude(r, (-5, -10, 6), 'XY', "sketch().push([(-5, -10)]).circle(5).finalize()", 24)
