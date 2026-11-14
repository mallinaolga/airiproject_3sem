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
r=extrude(r, (0, -120, 0), 'ZX', "sketch().push([(-5, -18.5)]).rect(38, 7).finalize()", 240)
r=extrude(r, (-19, 73, -5), 'ZX', "sketch().push([(-5, -19)]).rect(60, 12).finalize()", 34, False)
r=extrude(r, (-21, -77, 14), 'YZ', "sketch().push([(-77, 2.5)]).rect(8, 23).finalize()", 34)
r=extrude(r, (-13, 78, 13), 'YZ', "sketch().segment((56, 29), (62, 35)).segment((100, -3)).segment((94, -9)).close().assemble().finalize()", 18)
r=extrude(r, (5, 76, 20), 'YZ', "sketch().push([(76, 20)]).rect(4, 14).finalize()", 19)
