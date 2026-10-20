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
r=extrude(r, (100, 0, 0), 'YZ', "sketch().push([(0, 0)]).circle(70).finalize()", -188)
r=extrude(r, (-88, 30, 23), 'YZ', "sketch().push([(30, 23)]).rect(6, 20).finalize()", -12)
