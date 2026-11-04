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
r=extrude(r, (-90, 0, 0), 'YZ', "sketch().push([(0, -5)]).rect(38, 14).finalize()", 146)
r=extrude(r, (-83, 0, -5), 'YZ', "sketch().push([(0, -5)]).rect(54, 20).finalize()", 25, False)
r=extrude(r, (36, -19, 0), 'ZX', "sketch().push([(0, 36)]).circle(54).finalize()", -1)
r=extrude(r, (-86, -19, -9), 'ZX', "sketch().push([(-9, -86)]).circle(1).finalize()", -3)
r=extrude(r, (33, -19, 37), 'ZX', "sketch().push([(37, 33)]).circle(11).finalize()", -3)
r=extrude(r, (29, -22, 45), 'ZX', "sketch().push([(45, 29)]).circle(2).finalize()", -4)
