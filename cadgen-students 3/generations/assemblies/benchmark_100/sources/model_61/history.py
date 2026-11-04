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
r=extrude(r, (0, 0, -111), 'XY', "sketch().push([(-7, 0)]).rect(146, 124).finalize()", 221)
r=extrude(r, (-7, 0, 3), 'XY', "sketch().push([(-7, 0)]).rect(206, 174).finalize()", 29, False)
r=extrude(r, (66, 0, 96), 'YZ', "sketch().push([(0, 96)]).rect(38, 12).finalize()", 46)
r=extrude(r, (-80, 6, -92), 'YZ', "sketch().segment((4, -96), (6, -87)).segment((8, -88)).segment((6, -97)).close().assemble().finalize()", -32)
r=extrude(r, (77, -19, 32), 'XY', "sketch().push([(77, -19)]).rect(42, 40).finalize()", 7)
