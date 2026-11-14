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
r=extrude(r, (0, 72, 0), 'ZX', "sketch().push([(-15, 0)]).circle(58).finalize()", -187)
r=extrude(r, (0, -58, -15), 'ZX', "sketch().push([(-15, 0)]).circle(75).finalize()", -19, False)
r=extrude(r, (0, 41, 44), 'XY', "sketch().push([(0, 41)]).circle(1).finalize()", 47)
r=extrude(r, (0, 68, 44), 'XY', "sketch().segment((-25, 32), (-15, 68)).segment((-15, 81)).segment((-12, 81)).segment((-4, 112)).segment((25, 104)).segment((15, 68)).segment((15, 55)).segment((12, 55)).segment((4, 24)).close().assemble().finalize()", 23)
r=extrude(r, (52, 72, -10), 'ZX', "sketch().segment((-15, 52), (-13, 54)).arc((-13, 55), (-12, 55)).segment((-10, 57)).segment((-9, 56)).arc((-7, 55), (-6, 53)).segment((-5, 52)).segment((-7, 50)).arc((-7, 49), (-8, 49)).segment((-10, 47)).segment((-11, 48)).arc((-13, 49), (-14, 51)).close().assemble().finalize()", 42)
