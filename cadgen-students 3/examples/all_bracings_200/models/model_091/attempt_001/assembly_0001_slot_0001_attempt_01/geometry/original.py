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
r=extrude(r, (0, 51, 0), 'ZX', "sketch().push([(4.5, -14)]).rect(25, 50).finalize()", -141)
r=extrude(r, (-14, -59, 5), 'ZX', "sketch().push([(5, -14)]).rect(28, 54).finalize()", -22, False)
r=extrude(r, (13, -81, 11), 'YZ', "sketch().push([(-81, 11)]).circle(20).finalize()", 7)
r=extrude(r, (10, 51, -4), 'ZX', "sketch().push([(-4, 10)]).circle(32).finalize()", 50)
r=extrude(r, (-1, 32, 17), 'XY', "sketch().push([(-1, 32)]).rect(2, 16).finalize()", 18)
