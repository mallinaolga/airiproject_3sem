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
r=extrude(r, (0, 33, 0), 'ZX', "sketch().push([(65, 81)]).circle(6).finalize()", -31)
r=extrude(r, (81, 22, 65), 'ZX', "sketch().push([(65, 81)]).circle(7).finalize()", -3, False)
r=extrude(r, (81, 33, 59), 'XY', "sketch().segment((43, 2), (43, 64)).segment((67, 64)).arc((81, 67), (95, 64)).segment((119, 64)).segment((119, 2)).segment((95, 2)).arc((81, -1), (67, 2)).close().assemble().finalize()", -121)
r=extrude(r, (44, 63, 0), 'YZ', "sketch().push([(62.5, 0)]).rect(1, 238).finalize()", -162)
r=extrude(r, (44, 28, -52), 'ZX', "sketch().push([(-52, 33.5)]).rect(82, 21).finalize()", -96)
