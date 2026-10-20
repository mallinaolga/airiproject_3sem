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
r=extrude(r, (0, -43, 0), 'ZX', "sketch().push([(0, 25)]).rect(178, 150).finalize()", 71)
r=extrude(r, (-50, 0, 37), 'YZ', "sketch().segment((-59, 31), (-58, 46)).segment((-30, 45)).segment((-30, 48)).segment((52, 48)).arc((53, 46), (54, 48)).segment((59, 48)).segment((59, 27)).segment((35, 27)).segment((35, 26)).segment((21, 27)).segment((-30, 27)).segment((-30, 29)).close().assemble().finalize()", -50)
