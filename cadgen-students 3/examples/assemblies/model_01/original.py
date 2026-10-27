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
r=extrude(r, (39, 0, 0), 'YZ', "sketch().push([(0, -36)]).rect(10, 34).finalize()", -152)
r=extrude(r, (-68, 0, -36), 'YZ', "sketch().push([(0, -36)]).rect(14, 50).finalize()", -16, False)
r=extrude(r, (39, 3, -30), 'YZ', "sketch().segment((-76, -67), (-74, 11)).segment((82, 7)).segment((80, -71)).close().assemble().finalize()", 22)
r=extrude(r, (39, -30, -64), 'YZ', "sketch().push([(-30, -64)]).circle(25).finalize()", -53)
r=extrude(r, (34, -30, -38), 'YZ', "sketch().segment((-43, -43), (-39, -23)).arc((-43, -14), (-39, -5)).arc((-30, -1), (-21, -5)).arc((-17, -14), (-21, -23)).segment((-17, -43)).arc((-30, -38), (-43, -43)).assemble().finalize()", -23)
r=extrude(r, (61, 21, -6), 'YZ', "sketch().push([(21, -6)]).circle(59).finalize()", 8)
r=extrude(r, (69, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(94).finalize()", 44)
