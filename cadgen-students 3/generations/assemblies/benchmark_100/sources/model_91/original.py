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
r=extrude(r, (0, 0, 107), 'XY', "sketch().push([(32.5, 26)]).rect(7, 48).finalize()", -213)
r=extrude(r, (33, 26, -81), 'XY', "sketch().push([(33, 26)]).rect(10, 68).finalize()", -29, False)
r=extrude(r, (39, 16, -96), 'YZ', "sketch().segment((5, -110), (10, -79)).segment((27, -82)).segment((22, -113)).close().assemble().finalize()", 11)
r=extrude(r, (28, 0, -103), 'YZ', "sketch().arc((-116, -105), (0, -101), (116, -105)).close().assemble().finalize()", -51)
r=extrude(r, (32, 26, 106), 'YZ', "sketch().push([(26, 106)]).circle(1).finalize()", -13)
r=extrude(r, (32, 5, 94), 'YZ', "sketch().push([(35, 94)]).rect(60, 38).finalize()", -14)
r=extrude(r, (32, 25, -39), 'XY', "sketch().push([(-8, 25)]).rect(80, 8).finalize()", 37)
r=extrude(r, (-41, 21, -4), 'XY', "sketch().push([(-41, 21.5)]).rect(8, 1).finalize()", 87)
