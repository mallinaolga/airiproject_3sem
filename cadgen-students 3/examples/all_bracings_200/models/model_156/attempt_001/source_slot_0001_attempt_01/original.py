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
r=extrude(r, (72, 0, 0), 'YZ', "sketch().push([(0, 39)]).circle(36).finalize()", -144)
r=extrude(r, (-40, 0, 39), 'YZ', "sketch().push([(0, 39)]).circle(54).finalize()", -30, False)
r=extrude(r, (-41, 0, -15), 'XY', "sketch().push([(-41, 0)]).rect(30, 26).push([(-26, 1)]).circle(1, mode='s').finalize()", -78)
r=extrude(r, (17, 0, 3), 'XY', "sketch().push([(17, 0)]).rect(32, 26).finalize()", -46)
