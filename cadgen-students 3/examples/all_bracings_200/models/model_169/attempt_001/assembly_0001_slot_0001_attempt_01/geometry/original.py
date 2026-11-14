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
r=extrude(r, (105, 0, 0), 'YZ', "sketch().push([(-1, 2)]).rect(10, 22).finalize()", -210)
r=extrude(r, (104, -1, 2), 'YZ', "sketch().push([(-1, 2)]).rect(18, 38).finalize()", -44, False)
r=extrude(r, (63, -10, -10), 'ZX', "sketch().push([(-10, 63)]).rect(20, 26).finalize()", -1)
r=extrude(r, (-62, 2, 13), 'XY', "sketch().segment((-71, -4), (-60, 13)).segment((-53, 8)).segment((-64, -9)).close().assemble().finalize()", 4)
r=extrude(r, (66, -10, 0), 'YZ', "sketch().push([(-10, 7)]).rect(26, 14).finalize()", 11)
r=extrude(r, (-75, 4, -6), 'ZX', "sketch().push([(-6, -75)]).circle(8).finalize()", 19)
