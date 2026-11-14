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
r=extrude(r, (-23, 0, 0), 'YZ', "sketch().push([(10.5, 34)]).rect(53, 6).finalize()", 113)
r=extrude(r, (14, 10, 34), 'YZ', "sketch().push([(10, 34)]).rect(68, 8).finalize()", 12, False)
r=extrude(r, (34, 15, 31), 'XY', "sketch().push([(34, 15)]).circle(4).finalize()", -31)
r=extrude(r, (41, 0, 37), 'XY', "sketch().segment((-17, 53), (89, 62)).segment((91, 45)).segment((77, 45)).segment((77, 25)).segment((92, 25)).segment((99, -53)).segment((-7, -62)).close().assemble().finalize()", 24)
r=extrude(r, (82, -14, 31), 'XY', "sketch().segment((79, -16), (79, -12)).segment((85, -12)).arc((84, -14), (85, -16)).close().assemble().finalize()", -42)
r=extrude(r, (-7, 0, 31), 'XY', "sketch().segment((-99, 39), (58, 76)).segment((85, -39)).segment((-72, -76)).close().assemble().push([(-53, -50)]).circle(6, mode='s').finalize()", -51)
r=extrude(r, (-47, -50, 29), 'XY', "sketch().arc((-50, -55), (-47, -50), (-50, -45)).segment((-37, -45)).arc((-38, -50), (-37, -55)).close().assemble().finalize()", -110)
r=extrude(r, (-63, -25, 31), 'XY', "sketch().segment((-80, -41), (-80, -9)).segment((-46, -9)).arc((-52, -25), (-46, -41)).close().assemble().finalize()", 49)
