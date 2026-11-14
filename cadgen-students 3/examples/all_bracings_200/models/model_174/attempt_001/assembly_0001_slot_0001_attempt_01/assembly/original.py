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
r=extrude(r, (0, 98, 0), 'ZX', "sketch().push([(-16, 0)]).circle(40).finalize()", -196)
r=extrude(r, (0, 5, -16), 'ZX', "sketch().push([(-16, 0)]).circle(44).finalize()", -23, False)
r=extrude(r, (0, -39, 24), 'ZX', "sketch().arc((14, -26), (24, 0), (14, 26)).segment((60, 26)).segment((60, -26)).close().assemble().finalize()", 16)
