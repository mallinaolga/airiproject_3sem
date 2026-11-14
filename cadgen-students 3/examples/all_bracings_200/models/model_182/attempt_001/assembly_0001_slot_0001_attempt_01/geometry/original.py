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
r=extrude(r, (104, 0, 0), 'YZ', "sketch().push([(15, 5)]).rect(26, 22).finalize()", -208)
r=extrude(r, (-68, 15, 5), 'YZ', "sketch().push([(15, 5)]).rect(36, 30).finalize()", -21, False)
r=extrude(r, (80, 20, 16), 'XY', "sketch().push([(80, 20)]).rect(4, 2).finalize()", 3)
r=extrude(r, (43, 2, 5), 'XY', "sketch().segment((28, 2), (58, 2)).segment((54, -6)).arc((58, -17), (54, -28)).arc((43, -32), (32, -28)).arc((28, -17), (32, -6)).close().assemble().finalize()", -23)
r=extrude(r, (51, 3, -15), 'ZX', "sketch().push([(-15, 51)]).rect(10, 84).finalize()", 7)
