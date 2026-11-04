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
r=extrude(r, (-105, 0, 0), 'YZ', "sketch().push([(2, -1.5)]).rect(26, 29).finalize()", 211)
r=extrude(r, (-86, 2, -1), 'YZ', "sketch().push([(2, -1)]).rect(44, 46).finalize()", 31, False)
r=extrude(r, (53, -4, 13), 'XY', "sketch().segment((46, -24), (46, -20)).arc((35, -4), (46, 12)).segment((46, 16)).segment((60, 16)).segment((60, 12)).arc((71, -4), (60, -20)).segment((60, -24)).close().assemble().finalize()", 14)
r=extrude(r, (62, 5, -16), 'XY', "sketch().push([(62, 5)]).rect(30, 12).finalize()", -11)
