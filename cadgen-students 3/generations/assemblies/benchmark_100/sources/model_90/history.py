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
r=extrude(r, (90, 0, 0), 'YZ', "sketch().push([(40, -11)]).rect(60, 14).finalize()", -181)
r=extrude(r, (-6, 40, -11), 'YZ', "sketch().push([(40, -11)]).rect(82, 18).finalize()", -29, False)
r=extrude(r, (54, 35, -18), 'XY', "sketch().segment((44, 35), (52, 45)).segment((64, 35)).segment((56, 25)).close().assemble().finalize()", -16)
r=extrude(r, (-13, -1, -11), 'ZX', "sketch().push([(-11, -13)]).rect(16, 10).finalize()", -80)
r=extrude(r, (16, 35, -4), 'XY', "sketch().segment((2, 31), (2, 39)).segment((15, 39)).segment((15, 47)).segment((17, 47)).segment((17, 39)).segment((30, 39)).segment((30, 31)).segment((17, 31)).segment((17, 23)).segment((15, 23)).segment((15, 31)).close().assemble().finalize()", 38)
