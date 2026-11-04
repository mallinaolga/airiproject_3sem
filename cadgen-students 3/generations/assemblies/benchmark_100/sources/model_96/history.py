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
r=extrude(r, (0, -5, 0), 'ZX', "sketch().push([(21, -7)]).circle(22).finalize()", 108)
r=extrude(r, (-7, 92, 21), 'ZX', "sketch().push([(21, -7)]).circle(27).finalize()", 14, False)
r=extrude(r, (-13, -5, 36), 'ZX', "sketch().push([(36, -13)]).circle(2).finalize()", -14)
r=extrude(r, (-3, -5, 16), 'XY', "sketch().push([(-3, -54)]).rect(74, 98).finalize()", 25)
r=extrude(r, (-40, -94, 24), 'YZ', "sketch().push([(-94, 24)]).circle(12).finalize()", -19)
r=extrude(r, (34, -32, 22), 'YZ', "sketch().push([(-32, 22)]).circle(11).finalize()", 25)
r=extrude(r, (23, -5, 16), 'YZ', "sketch().push([(-5, -16.5)]).rect(74, 65).finalize()", -6)
r=extrude(r, (-34, -15, 16), 'XY', "sketch().push([(-34, -15)]).circle(3).finalize()", -43)
