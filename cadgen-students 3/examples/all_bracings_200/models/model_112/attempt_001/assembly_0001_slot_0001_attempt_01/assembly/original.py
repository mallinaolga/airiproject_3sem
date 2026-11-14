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
r=extrude(r, (0, 0, -14), 'XY', "sketch().push([(8, -28)]).circle(4).finalize()", 41)
r=extrude(r, (8, -28, 21), 'XY', "sketch().push([(8, -28)]).circle(4).finalize()", 8, False)
r=extrude(r, (12, -28, 12), 'YZ', "sketch().push([(-28, 12)]).rect(8, 2).finalize()", 86)
r=extrude(r, (97, -29, 13), 'XY', "sketch().push([(97, -29)]).circle(1).finalize()", 16)
r=extrude(r, (53, -25, 10), 'YZ', "sketch().segment((-73, 10), (23, 10)).segment((9, -19)).arc((23, -54), (9, -88)).arc((-25, -102), (-59, -88)).arc((-73, -54), (-59, -19)).close().assemble().finalize()", -157)
r=extrude(r, (73, -32, 11), 'YZ', "sketch().arc((-40, 8), (-41, 11), (-40, 14)).arc((-37, 15), (-35, 14)).segment((-32, 102)).segment((-32, -80)).segment((-35, 8)).arc((-37, 7), (-40, 8)).assemble().finalize()", 25)
r=extrude(r, (53, 23, -53), 'ZX', "sketch().segment((-69, 5), (-43, 103)).segment((-37, 101)).segment((-63, 3)).close().assemble().finalize()", 50)
