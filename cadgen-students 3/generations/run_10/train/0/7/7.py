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
r=extrude(r, (0, 21, 0), 'ZX', "sketch().push([(4.5, 29)]).rect(57, 64).finalize()", -121)
r=extrude(r, (53, 6, 28), 'YZ', "sketch().push([(6, -1)]).rect(188, 58).finalize()", -114)
