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
r=extrude(r, (-8, 0, 0), 'YZ', "sketch().push([(4, 9)]).circle(29).finalize()", -89)
r=extrude(r, (-84, 4, 9), 'YZ', "sketch().push([(4, 9)]).circle(34).finalize()", -12, False)
r=extrude(r, (-8, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(194, 204).finalize()", 48)
r=extrude(r, (39, 24, -39), 'YZ', "sketch().push([(24, -39)]).rect(118, 42).finalize()", 58)
