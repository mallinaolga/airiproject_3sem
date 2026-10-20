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
r=extrude(r, (0, -51, 0), 'ZX', "sketch().segment((-36, -100), (-36, -52)).arc((-63, 0), (-36, 52)).segment((-36, 100)).segment((36, 100)).segment((36, 89)).arc((22, 74), (36, 59)).segment((36, 52)).arc((63, 0), (36, -52)).segment((36, -100)).close().assemble().finalize()", 101)
