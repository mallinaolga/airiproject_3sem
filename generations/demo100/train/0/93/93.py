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
r=extrude(r, (22, 0, 0), 'YZ', "sketch().push([(-43, -10)]).rect(42, 134).finalize()", -122)
r=extrude(r, (-25, -27, 37), 'YZ', "sketch().segment((-27, -4), (-27, 78)).segment((-2, 66)).arc((27, 78), (55, 66)).arc((67, 37), (55, 8)).arc((27, -4), (-2, 8)).close().assemble().finalize()", -40)
r=extrude(r, (-25, -14, 66), 'YZ', "sketch().push([(-14, 66)]).rect(2, 22).finalize()", 126)
