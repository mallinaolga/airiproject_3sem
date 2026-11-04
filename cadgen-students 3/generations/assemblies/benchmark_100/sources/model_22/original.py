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
r=extrude(r, (0, 0, -106), 'XY', "sketch().push([(32, -46.5)]).rect(56, 17).finalize()", 194)
r=extrude(r, (32, -46, 85), 'XY', "sketch().push([(32, -46)]).rect(92, 28).finalize()", 23, False)
r=extrude(r, (4, -47, -78), 'XY', "sketch().segment((-25, -70), (-25, -15)).segment((4, -15)).segment((4, -79)).segment((-22, -79)).arc((-23, -74), (-25, -70)).assemble().finalize()", 7)
r=extrude(r, (-17, -16, -72), 'YZ', "sketch().push([(31.5, -72)]).rect(95, 70).finalize()", 33)
r=extrude(r, (-17, 68, -41), 'YZ', "sketch().push([(68, -41)]).rect(6, 4).finalize()", -61)
r=extrude(r, (-17, -1, -66), 'ZX', "sketch().segment((-84, -17), (-48, -17)).segment((-53, -30)).arc((-48, -42), (-53, -55)).arc((-66, -60), (-79, -55)).arc((-84, -42), (-79, -30)).close().assemble().finalize()", 28)
