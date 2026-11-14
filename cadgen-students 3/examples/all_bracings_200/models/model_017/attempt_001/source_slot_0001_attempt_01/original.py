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
r=extrude(r, (42, 0, 0), 'YZ', "sketch().push([(54.5, 4.5)]).rect(41, 47).finalize()", -85)
r=extrude(r, (23, 54, 5), 'YZ', "sketch().push([(54, 5)]).rect(64, 72).finalize()", -10, False)
r=extrude(r, (-25, 75, 20), 'YZ', "sketch().push([(-4.5, 20)]).rect(159, 200).finalize()", -5)
r=extrude(r, (-25, -42, -71), 'YZ', "sketch().segment((-86, -120), (-86, -71)).segment((-15, -89)).segment((2, -22)).segment((2, -120)).close().assemble().finalize()", 79)
r=extrude(r, (-30, 22, 57), 'YZ', "sketch().push([(22, 57)]).rect(14, 96).finalize()", -24)
r=extrude(r, (20, 23, -32), 'YZ', "sketch().segment((10, -32), (14, -14)).arc((10, -5), (14, 5)).arc((23, 8), (32, 5)).arc((36, -5), (32, -14)).segment((36, -32)).close().assemble().finalize()", -16)
