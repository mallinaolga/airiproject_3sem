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
r=extrude(r, (91, 0, 0), 'YZ', "sketch().push([(20, 6.5)]).rect(2, 37).finalize()", -181)
r=extrude(r, (-48, 20, 7), 'YZ', "sketch().push([(20, 7)]).rect(4, 48).finalize()", -35, False)
r=extrude(r, (60, 18, -4), 'ZX', "sketch().push([(-4, 60)]).circle(13).finalize()", -15)
r=extrude(r, (-23, 18, -11), 'ZX', "sketch().push([(-11, -23)]).circle(23).finalize()", -22)
r=extrude(r, (-56, 18, 12), 'YZ', "sketch().arc((-16, 0), (-21, 12), (-16, 24)).arc((-3, 29), (9, 24)).segment((18, 34)).segment((18, -10)).segment((9, 0)).arc((-3, -5), (-16, 0)).assemble().finalize()", 12)
r=extrude(r, (-80, 18, 9), 'ZX', "sketch().push([(9, -80)]).rect(46, 24).finalize()", -30)
