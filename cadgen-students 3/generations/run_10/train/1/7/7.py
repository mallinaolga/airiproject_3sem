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
r=extrude(r, (0, 95, 0), 'ZX', "sketch().arc((-93, 21), (-88, 23), (-91, 27)).arc((-53, 11), (-93, 21)).assemble().finalize()", 5)
r=extrude(r, (24, 98, -88), 'ZX', "sketch().arc((-89, 22), (-88, 24), (-89, 26)).segment((93, 26)).segment((93, 22)).close().assemble().finalize()", -138)
r=extrude(r, (22, -32, 3), 'YZ', "sketch().push([(-32, 3)]).rect(136, 88).finalize()", -60)
