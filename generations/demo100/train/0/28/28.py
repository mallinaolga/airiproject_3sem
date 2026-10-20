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
r=extrude(r, (0, -100, 0), 'ZX', "sketch().push([(0, 0)]).rect(102, 48).push([(2, -13)]).circle(2, mode='s').push([(-26, -5)]).parray(11, 30, 360, 27).rect(2, 2, mode='s').finalize()", 200)
