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
r=extrude(r, (-105, 0, 0), 'YZ', "sketch().push([(-4, 20)]).rect(22, 18).finalize()", 211)
r=extrude(r, (30, -4, 20), 'YZ', "sketch().push([(-4, 20)]).rect(26, 22).finalize()", 30, False)
r=extrude(r, (32, 5, 9), 'XY', "sketch().push([(32, 5)]).circle(1).finalize()", -40)
r=extrude(r, (-77, 8, 22), 'YZ', "sketch().segment((8, 20), (8, 24)).segment((14, 23)).arc((16, 24), (17, 23)).arc((18, 22), (17, 21)).arc((16, 20), (14, 21)).close().assemble().finalize()", 12)
