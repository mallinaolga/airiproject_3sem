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
r=extrude(r, (0, -22, 0), 'ZX', "sketch().push([(0, -23)]).circle(28).finalize()", 92)
r=extrude(r, (-23, -5, 0), 'ZX', "sketch().push([(0, -23)]).circle(47).finalize()", 25, False)
r=extrude(r, (-23, 8, -47), 'XY', "sketch().segment((-30, -13), (-28, 30)).segment((-16, 29)).segment((-18, -14)).close().assemble().finalize()", -47)
r=extrude(r, (24, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(102).finalize()", 4)
r=extrude(r, (29, -13, -79), 'YZ', "sketch().push([(-13, -79)]).circle(17).finalize()", 42)
r=extrude(r, (-23, 7, 47), 'XY', "sketch().push([(-23, 7)]).circle(5).finalize()", 48)
