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
r=extrude(r, (92, 0, 0), 'YZ', "sketch().push([(6, 0)]).circle(26).finalize()", -184)
r=extrude(r, (-44, 6, 0), 'YZ', "sketch().push([(6, 0)]).circle(43).finalize()", -27, False)
r=extrude(r, (13, -20, 0), 'ZX', "sketch().push([(0, 13)]).circle(23).finalize()", -10)
r=extrude(r, (27, -30, 6), 'ZX', "sketch().push([(6, 27)]).circle(4).finalize()", -19)
