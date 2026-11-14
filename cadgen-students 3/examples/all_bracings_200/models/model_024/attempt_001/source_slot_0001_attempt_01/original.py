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
r=extrude(r, (0, -95, 0), 'ZX', "sketch().push([(7.5, 0)]).rect(11, 14).finalize()", 136)
r=extrude(r, (0, -23, 7), 'ZX', "sketch().push([(7, 0)]).rect(16, 22).finalize()", 40, False)
r=extrude(r, (5, 8, 0), 'YZ', "sketch().segment((-79, 0), (95, 0)).segment((13, -3)).arc((15, -8), (13, -13)).arc((8, -15), (3, -13)).arc((1, -8), (3, -3)).close().assemble().finalize()", -4)
