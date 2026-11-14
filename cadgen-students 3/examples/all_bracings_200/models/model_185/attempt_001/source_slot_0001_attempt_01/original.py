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
r=extrude(r, (-105, 0, 0), 'YZ', "sketch().push([(0, 4)]).circle(24).finalize()", 214)
r=extrude(r, (39, 0, 4), 'YZ', "sketch().push([(0, 4)]).circle(40).finalize()", 30, False)
r=extrude(r, (-49, 0, -21), 'XY', "sketch().push([(-49, 0)]).rect(4, 12).finalize()", -20)
r=extrude(r, (61, 40, 4), 'ZX', "sketch().push([(4, 61)]).circle(12).finalize()", 1)
r=extrude(r, (-93, 24, 4), 'ZX', "sketch().push([(4, -93)]).circle(17).finalize()", 15)
r=extrude(r, (69, 0, -36), 'XY', "sketch().push([(69, 0)]).circle(41).push([(69, 0)]).circle(12, mode='s').finalize()", -7)
