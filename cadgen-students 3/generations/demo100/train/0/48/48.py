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
r=extrude(r, (55, 0, 0), 'YZ', "sketch().segment((-100, 43), (-98, 48)).segment((-28, 16)).arc((-26, 21), (-22, 24)).segment((-17, 11)).segment((15, -3)).segment((1, 33)).arc((27, 18), (31, -11)).segment((100, -43)).segment((98, -48)).segment((28, -16)).arc((26, -21), (22, -24)).segment((17, -11)).segment((-15, 3)).segment((-1, -33)).arc((-27, -18), (-31, 11)).close().assemble().finalize()", -109)
