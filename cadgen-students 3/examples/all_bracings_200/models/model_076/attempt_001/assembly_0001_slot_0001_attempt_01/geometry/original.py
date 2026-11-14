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
r=extrude(r, (106, 0, 0), 'YZ', "sketch().push([(5, -12)]).rect(66, 54).finalize()", -212)
r=extrude(r, (31, 5, -12), 'YZ', "sketch().push([(5, -12)]).rect(90, 74).finalize()", -42, False)
r=extrude(r, (27, -40, -33), 'ZX', "sketch().push([(-33, 27)]).circle(1).finalize()", -10)
r=extrude(r, (30, -16, -48), 'XY', "sketch().segment((29, -17), (29, -16)).segment((29, -15)).segment((31, -15)).segment((31, -16)).segment((31, -17)).close().assemble().finalize()", -17)
r=extrude(r, (-1, 24, -48), 'XY', "sketch().segment((-2, 24), (-1, 25)).segment((0, 24)).segment((-1, 23)).close().assemble().finalize()", -30)
r=extrude(r, (26, -11, 25), 'XY', "sketch().push([(26, -11)]).circle(1).finalize()", 54)
