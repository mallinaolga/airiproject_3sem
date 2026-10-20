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
r=extrude(r, (50, 0, 0), 'YZ', "sketch().push([(-25, 0)]).rect(150, 104).finalize()", -99)
r=extrude(r, (-37, 50, -15), 'ZX', "sketch().segment((-21, -41), (-21, -28)).segment((-9, -28)).segment((-9, -31)).arc((-10, -32), (-10, -33)).segment((-15, -36)).segment((-9, -45)).segment((-9, -46)).arc((-14, -42), (-21, -41)).assemble().finalize()", 50)
