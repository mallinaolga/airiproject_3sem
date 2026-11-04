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
r=extrude(r, (114, 0, 0), 'YZ', "sketch().push([(2, -1)]).rect(24, 30).finalize()", -228)
r=extrude(r, (79, 2, -1), 'YZ', "sketch().push([(2, -1)]).rect(42, 50).finalize()", -23, False)
r=extrude(r, (70, -19, 14), 'ZX', "sketch().push([(14, 70)]).rect(24, 26).push([(9, 71)]).circle(5, mode='s').finalize()", -4)
r=extrude(r, (80, -19, 22), 'YZ', "sketch().segment((-19, 19), (-19, 25)).segment((-14, 24)).arc((-12, 25), (-9, 24)).arc((-8, 22), (-9, 20)).arc((-12, 19), (-14, 20)).close().assemble().finalize()", 29)
r=extrude(r, (102, -10, 2), 'ZX', "sketch().push([(2, 102)]).circle(9).finalize()", -10)
r=extrude(r, (33, -4, 14), 'XY', "sketch().segment((29, -3), (29, -2)).segment((31, -2)).arc((34, -2), (35, -4)).segment((37, -5)).segment((37, -6)).segment((35, -6)).arc((32, -6), (31, -4)).close().assemble().finalize()", 4)
r=extrude(r, (36, -10, -6), 'ZX', "sketch().push([(-6, 36)]).circle(8).finalize()", -2)
