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
r=extrude(r, (0, 0, 44), 'XY', "sketch().push([(0, -32)]).circle(8).finalize()", -69)
r=extrude(r, (0, -32, 30), 'XY', "sketch().push([(0, -32)]).circle(9).finalize()", -7, False)
r=extrude(r, (0, -24, 40), 'ZX', "sketch().segment((11, 66), (17, 69)).segment((69, -66)).segment((63, -69)).close().assemble().finalize()", 115)
r=extrude(r, (0, -40, 0), 'ZX', "sketch().segment((-112, -54), (-112, 54)).segment((-15, 54)).segment((-15, 101)).segment((15, 101)).segment((15, 54)).segment((112, 54)).segment((112, -54)).segment((15, -54)).segment((15, -101)).segment((-15, -101)).segment((-15, -54)).close().assemble().finalize()", -51)
