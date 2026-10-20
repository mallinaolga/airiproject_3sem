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
r=extrude(r, (0, 0, 72), 'XY', "sketch().segment((-83, -31), (-60, -20)).segment((-60, 39)).segment((-33, 39)).segment((-33, 51)).segment((-31, 51)).segment((-31, 100)).segment((31, 100)).segment((31, 51)).segment((33, 51)).segment((33, 39)).segment((60, 39)).segment((60, 33)).segment((79, 41)).segment((83, 31)).segment((60, 20)).segment((60, -39)).segment((33, -39)).segment((33, -51)).segment((31, -51)).segment((31, -100)).segment((-31, -100)).segment((-31, -51)).segment((-33, -51)).segment((-33, -39)).segment((-60, -39)).segment((-60, -33)).segment((-79, -41)).close().assemble().finalize()", -143)
