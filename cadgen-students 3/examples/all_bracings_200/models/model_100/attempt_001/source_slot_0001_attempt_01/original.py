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
r=extrude(r, (0, -96, 0), 'ZX', "sketch().push([(0.5, 6.5)]).rect(33, 25).finalize()", 191)
r=extrude(r, (7, -91, 0), 'ZX', "sketch().push([(0, 7)]).rect(58, 44).finalize()", 46, False)
r=extrude(r, (9, -29, -16), 'XY', "sketch().push([(9, -29)]).rect(12, 10).finalize()", -10)
r=extrude(r, (-15, -58, 0), 'YZ', "sketch().segment((-73, -5), (-73, 5)).segment((-63, 5)).arc((-58, 7), (-53, 5)).segment((-43, 5)).segment((-43, -5)).segment((-53, -5)).arc((-58, -7), (-63, -5)).close().assemble().finalize()", -13)
r=extrude(r, (-23, -48, -5), 'XY', "sketch().push([(-23, -48)]).circle(3).finalize()", -23)
