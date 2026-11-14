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
r=extrude(r, (0, -118, 0), 'ZX', "sketch().push([(22, -11)]).circle(23).finalize()", 235)
r=extrude(r, (-11, -94, 22), 'ZX', "sketch().push([(22, -11)]).circle(34).finalize()", 31, False)
r=extrude(r, (12, 13, 22), 'YZ', "sketch().push([(13, 22)]).rect(4, 6).push([(13, 22)]).circle(1, mode='s').finalize()", 32)
r=extrude(r, (-11, -85, -12), 'ZX', "sketch().arc((-56, -35), (-50, -11), (-56, 13)).segment((-1, 13)).arc((-12, -11), (-1, -35)).close().assemble().finalize()", -23)
r=extrude(r, (13, -102, -23), 'YZ', "sketch().push([(-102, -23)]).circle(4).finalize()", 8)
