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
r=extrude(r, (0, 112, 0), 'ZX', "sketch().push([(0, 12)]).circle(62).finalize()", -197)
r=extrude(r, (12, 25, 0), 'ZX', "sketch().push([(0, 12)]).circle(92).finalize()", -36, False)
r=extrude(r, (-50, -75, 0), 'YZ', "sketch().segment((-112, 23), (-111, 25)).segment((-92, 12)).arc((-64, 17), (-57, -11)).segment((-38, -23)).segment((-39, -25)).segment((-58, -12)).arc((-86, -17), (-93, 11)).close().assemble().finalize()", -29)
r=extrude(r, (-50, -45, 0), 'ZX', "sketch().segment((-51, -104), (-51, -22)).arc((0, -50), (51, -22)).segment((51, -104)).close().assemble().finalize()", 18)
r=extrude(r, (-80, -79, 8), 'YZ', "sketch().push([(-79, 8)]).circle(11).finalize()", -18)
