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
r=extrude(r, (0, 94, 0), 'ZX', "sketch().push([(28.5, 6)]).rect(7, 40).finalize()", -188)
r=extrude(r, (6, 77, 29), 'ZX', "sketch().push([(29, 6)]).rect(8, 42).finalize()", -36, False)
r=extrude(r, (-15, 61, 29), 'YZ', "sketch().segment((59, 28), (62, 31)).segment((63, 30)).segment((60, 27)).close().assemble().finalize()", -12)
r=extrude(r, (2, 25, 27), 'XY', "sketch().segment((-7, 31), (-1, 36)).segment((11, 19)).segment((5, 14)).close().assemble().finalize()", -62)
