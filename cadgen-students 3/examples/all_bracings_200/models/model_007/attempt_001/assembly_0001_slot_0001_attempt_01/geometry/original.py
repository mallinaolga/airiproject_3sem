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
r=extrude(r, (-94, 0, 0), 'YZ', "sketch().push([(0, -1.5)]).rect(22, 17).finalize()", 189)
r=extrude(r, (12, 0, -2), 'YZ', "sketch().push([(0, -2)]).rect(30, 22).finalize()", 23, False)
r=extrude(r, (-86, 2, -12), 'XY', "sketch().push([(-86, 2)]).circle(3).finalize()", -2)
r=extrude(r, (16, -5, 10), 'XY', "sketch().segment((10, 1), (17, 3)).segment((18, 0)).arc((22, -3), (21, -8)).segment((22, -11)).segment((15, -13)).segment((14, -10)).arc((10, -7), (11, -2)).close().assemble().finalize()", 5)
