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
r=extrude(r, (0, 0, 57), 'XY', "sketch().segment((-100, -79), (-53, -16)).arc((-44, 5), (-27, 20)).segment((-25, 22)).segment((-24, 21)).arc((-11, 25), (2, 24)).arc((82, 80), (42, -8)).arc((14, -69), (-49, -46)).segment((-83, -92)).close().assemble().finalize()", -114)
