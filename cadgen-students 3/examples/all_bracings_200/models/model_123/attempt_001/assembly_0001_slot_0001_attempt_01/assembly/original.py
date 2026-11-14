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
r=extrude(r, (-76, 0, 0), 'YZ', "sketch().push([(-9.5, -1)]).rect(13, 12).finalize()", 126)
r=extrude(r, (37, -10, -1), 'YZ', "sketch().push([(-10, -1)]).rect(20, 18).finalize()", 34, False)
r=extrude(r, (47, -8, 9), 'XY', "sketch().push([(47, -8)]).rect(6, 16).finalize()", 1)
r=extrude(r, (-16, -14, -7), 'ZX', "sketch().push([(-8.5, -16)]).rect(3, 168).finalize()", -1)
r=extrude(r, (47, -1, 9), 'XY', "sketch().segment((-6, -1), (44, 0)).segment((44, 11)).segment((50, 11)).segment((50, 0)).segment((100, -1)).close().assemble().push([(47, 6)]).circle(2, mode='s').finalize()", 2)
r=extrude(r, (-76, -7, -4), 'ZX', "sketch().push([(-4, -60)]).rect(14, 32).finalize()", 26)
