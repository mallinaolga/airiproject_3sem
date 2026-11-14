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
r=extrude(r, (0, 0, 75), 'XY', "sketch().push([(-39, 16)]).circle(10).finalize()", -166)
r=extrude(r, (-39, 16, 71), 'XY', "sketch().push([(-39, 16)]).circle(14).finalize()", -27, False)
r=extrude(r, (-48, 26, 71), 'XY', "sketch().push([(-48, 26)]).circle(1).finalize()", 37)
r=extrude(r, (-29, 16, -90), 'YZ', "sketch().push([(16, -90)]).circle(1).finalize()", 81)
r=extrude(r, (-12, 15, -90), 'ZX', "sketch().push([(-90, -12)]).rect(36, 38).finalize()", -45)
