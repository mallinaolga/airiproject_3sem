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
r=extrude(r, (0, 75, 0), 'ZX', "sketch().push([(0, 0)]).circle(62).finalize()", -188)
r=extrude(r, (0, 41, 0), 'ZX', "sketch().push([(0, 0)]).circle(75).finalize()", -32, False)
r=extrude(r, (37, 75, -17), 'ZX', "sketch().push([(-17, 37)]).circle(12).finalize()", 26)
r=extrude(r, (-11, 75, 24), 'ZX', "sketch().segment((13, -30), (16, 9)).segment((35, 8)).segment((32, -31)).close().assemble().finalize()", 11)
r=extrude(r, (70, 41, -14), 'ZX', "sketch().push([(-14, 70)]).rect(62, 6).finalize()", 73)
