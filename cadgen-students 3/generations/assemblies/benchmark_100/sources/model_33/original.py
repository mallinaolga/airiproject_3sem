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
r=extrude(r, (0, 0, 108), 'XY', "sketch().push([(21.5, -27.5)]).rect(37, 55).finalize()", -216)
r=extrude(r, (22, -28, 53), 'XY', "sketch().push([(22, -28)]).rect(42, 64).finalize()", -26, False)
r=extrude(r, (2, -40, 78), 'YZ', "sketch().push([(-40, 78)]).circle(1).finalize()", -112)
r=extrude(r, (0, -16, 48), 'YZ', "sketch().push([(-16, 48)]).circle(8).push([(-16, 48)]).circle(2, mode='s').finalize()", -64)
r=extrude(r, (25, -5, 79), 'ZX', "sketch().push([(79, 25)]).rect(12, 2).finalize()", 64)
r=extrude(r, (31, -5, 107), 'XY', "sketch().push([(31, 4)]).rect(158, 18).finalize()", -5)
