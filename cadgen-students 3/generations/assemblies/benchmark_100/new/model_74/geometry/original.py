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
r=extrude(r, (-67, 0, 0), 'YZ', "sketch().push([(15, -27)]).circle(34).finalize()", 167)
r=extrude(r, (4, 15, -27), 'YZ', "sketch().push([(15, -27)]).circle(38).finalize()", 17, False)
r=extrude(r, (-40, 15, 7), 'XY', "sketch().push([(-40, 15)]).circle(51).finalize()", 19)
r=extrude(r, (-67, -1, -53), 'YZ', "sketch().push([(-1, -53)]).rect(12, 2).finalize()", -32)
r=extrude(r, (-40, -34, 10), 'XY', "sketch().segment((-54, -88), (-54, -31)).arc((-40, -34), (-26, -31)).segment((-26, -88)).close().assemble().finalize()", 14)
r=extrude(r, (-39, -57, 24), 'XY', "sketch().push([(-39, -57)]).rect(10, 10).finalize()", 41)
r=extrude(r, (-38, -61, 26), 'XY', "sketch().push([(-38, 14)]).rect(116, 150).finalize()", 37)
