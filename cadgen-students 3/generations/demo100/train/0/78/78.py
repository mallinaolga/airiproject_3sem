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
r=extrude(r, (32, 0, 0), 'YZ', "sketch().arc((-60, 25), (-57, 22), (-53, 21)).segment((-53, -3)).segment((-51, -3)).segment((-51, 21)).arc((-41, 31), (-49, 42)).arc((55, -34), (-60, 25)).assemble().reset().push([(0, -2)]).parray(30, 183, 212, 13).rect(6, 6, mode='s').finalize()", 68)
r=extrude(r, (32, -49, 16), 'YZ', "sketch().push([(-49, 16)]).rect(6, 24).finalize()", -132)
