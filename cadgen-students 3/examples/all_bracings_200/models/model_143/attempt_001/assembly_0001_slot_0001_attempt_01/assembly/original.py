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
r=extrude(r, (0, 60, 0), 'ZX', "sketch().push([(8.5, -10)]).rect(53, 58).finalize()", -180)
r=extrude(r, (-10, -71, 8), 'ZX', "sketch().push([(8, -10)]).rect(74, 80).finalize()", -21, False)
r=extrude(r, (30, -82, 33), 'YZ', "sketch().push([(-82, 33)]).circle(6).finalize()", 20)
r=extrude(r, (-5, 4, -18), 'ZX', "sketch().arc((-42, -14), (-45, -5), (-42, 4)).arc((-33, 7), (-24, 4)).segment((-18, 14)).segment((-18, -24)).segment((-24, -14)).arc((-33, -17), (-42, -14)).assemble().finalize()", -8)
r=extrude(r, (-14, 60, 19), 'ZX', "sketch().push([(19, -14)]).rect(12, 14).push([(19, -14)]).circle(4, mode='s').finalize()", 60)
r=extrude(r, (-1, 4, -38), 'ZX', "sketch().push([(-38, -1)]).rect(2, 4).finalize()", 9)
