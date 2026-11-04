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
r=extrude(r, (0, 0, 9), 'XY', "sketch().push([(2, 6)]).circle(13).finalize()", 109)
r=extrude(r, (2, 6, 26), 'XY', "sketch().push([(2, 6)]).circle(21).finalize()", 13, False)
r=extrude(r, (-19, 6, 36), 'YZ', "sketch().segment((-52, 22), (-52, 46)).segment((28, 46)).segment((42, 81)).segment((64, 72)).segment((53, 44)).segment((53, 22)).segment((44, 22)).segment((32, -9)).segment((9, 0)).segment((18, 22)).close().assemble().finalize()", -31)
r=extrude(r, (2, 28, 32), 'ZX', "sketch().push([(32, 2)]).rect(34, 22).finalize()", 25)
r=extrude(r, (-19, 0, 28), 'XY', "sketch().push([(16, 0)]).rect(70, 204).finalize()", -146)
