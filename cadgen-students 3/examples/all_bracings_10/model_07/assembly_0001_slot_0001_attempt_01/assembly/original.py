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
r=extrude(r, (92, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(66, 68).finalize()", -174)
r=extrude(r, (-70, 0, 0), 'YZ', "sketch().push([(0, 0)]).rect(88, 92).finalize()", -41, False)
r=extrude(r, (64, -33, 6), 'XY', "sketch().push([(64, 5)]).rect(26, 76).finalize()", 25)
r=extrude(r, (92, -22, 12), 'YZ', "sketch().segment((-21, 15), (-20, 14)).arc((-24, 10), (-21, 15)).assemble().finalize()", 20)
r=extrude(r, (37, 4, -34), 'XY', "sketch().segment((35, 11), (35, 15)).segment((37, 15)).segment((37, 12)).arc((45, 5), (39, -3)).segment((39, -7)).segment((37, -7)).segment((37, -4)).arc((29, 3), (35, 11)).assemble().finalize()", -9)
r=extrude(r, (53, -29, -34), 'XY', "sketch().push([(53, -29)]).rect(48, 24).push([(51, -28)]).circle(5, mode='s').finalize()", -6)
