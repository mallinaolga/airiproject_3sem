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
r=extrude(r, (0, 0, -32), 'XY', "sketch().push([(6, -19)]).circle(28).finalize()", 132)
r=extrude(r, (6, -19, 52), 'XY', "sketch().push([(6, -19)]).circle(31).finalize()", 26, False)
r=extrude(r, (6, -50, 68), 'ZX', "sketch().segment((48, 25), (59, 32)).segment((88, -13)).segment((77, -20)).close().assemble().finalize()", -2)
r=extrude(r, (34, -19, -7), 'YZ', "sketch().push([(-19, -7)]).rect(40, 2).finalize()", 2)
r=extrude(r, (0, 0, -32), 'XY', "sketch().segment((-73, -53), (-73, 53)).segment((33, 53)).segment((33, 25)).segment((73, 25)).segment((73, -38)).segment((33, -38)).segment((33, -53)).close().assemble().finalize()", -45)
r=extrude(r, (-63, -16, -77), 'XY', "sketch().push([(-63, -16)]).rect(8, 14).finalize()", -23)
