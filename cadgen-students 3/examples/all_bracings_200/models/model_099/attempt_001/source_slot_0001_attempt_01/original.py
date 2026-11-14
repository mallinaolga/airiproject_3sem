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
r=extrude(r, (-109, 0, 0), 'YZ', "sketch().push([(0, -4)]).circle(35).finalize()", 218)
r=extrude(r, (-47, 0, -4), 'YZ', "sketch().push([(0, -4)]).circle(49).finalize()", 26, False)
r=extrude(r, (-47, -45, -23), 'YZ', "sketch().push([(-45, -23)]).circle(3).finalize()", -26)
r=extrude(r, (51, 0, -38), 'XY', "sketch().push([(51, 0)]).circle(7).finalize()", -153)
r=extrude(r, (-40, 0, 47), 'XY', "sketch().push([(-40, 0)]).rect(78, 66).finalize()", 8)
