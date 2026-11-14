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
r=extrude(r, (0, -34, 0), 'ZX', "sketch().push([(75, -6)]).circle(10).finalize()", -81)
r=extrude(r, (-6, -45, 75), 'ZX', "sketch().push([(75, -6)]).circle(13).finalize()", -12, False)
r=extrude(r, (7, -45, 75), 'YZ', "sketch().push([(-45, 75)]).rect(86, 40).push([(-30, 77)]).circle(6, mode='s').finalize()", 12)
r=extrude(r, (-6, -34, 66), 'ZX', "sketch().segment((65, -5), (66, -5)).segment((67, -7)).segment((66, -7)).close().assemble().finalize()", 150)
r=extrude(r, (-6, -64, 65), 'ZX', "sketch().segment((-95, -14), (-95, 2)).segment((70, 2)).arc((65, -6), (70, -14)).close().assemble().finalize()", -28)
