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
r=extrude(r, (-24, 0, 0), 'YZ', "sketch().segment((-96, 78), (-96, 88)).segment((-10, 88)).arc((42, 73), (40, 18)).arc((56, -97), (-1, 4)).arc((-35, 34), (-24, 78)).close().assemble().finalize()", 47)
r=extrude(r, (5, -93, 88), 'XY', "sketch().push([(5, -93)]).circle(2).finalize()", 13)
