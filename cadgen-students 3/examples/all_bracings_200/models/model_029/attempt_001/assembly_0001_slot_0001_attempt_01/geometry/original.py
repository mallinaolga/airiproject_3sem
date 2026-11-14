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
r=extrude(r, (0, 0, 103), 'XY', "sketch().push([(-15.5, 1)]).rect(25, 50).finalize()", -206)
r=extrude(r, (-15, 1, -25), 'XY', "sketch().push([(-15, 1)]).rect(36, 72).finalize()", -27, False)
r=extrude(r, (-26, 20, 43), 'XY', "sketch().push([(3.5, 20)]).rect(59, 62).finalize()", 23)
r=extrude(r, (-18, -35, -43), 'ZX', "sketch().push([(-43, -18)]).circle(12).finalize()", -15)
