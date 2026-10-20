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
r=extrude(r, (0, 0, 26), 'XY', "sketch().segment((-74, -46), (-74, -35)).arc((-95, 24), (-33, 38)).segment((100, 38)).segment((100, -46)).close().assemble().finalize()", -52)
r=extrude(r, (-74, -39, 14), 'YZ', "sketch().push([(-39, 14)]).circle(4).finalize()", -24)
