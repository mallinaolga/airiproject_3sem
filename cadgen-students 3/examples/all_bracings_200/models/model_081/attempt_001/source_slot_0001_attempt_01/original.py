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
r=extrude(r, (0, 0, 93), 'XY', "sketch().push([(-33, 31.5)]).rect(28, 89).finalize()", -185)
r=extrude(r, (-33, 31, 19), 'XY', "sketch().push([(-33, 31)]).rect(42, 136).finalize()", -46, False)
r=extrude(r, (-24, -13, 52), 'ZX', "sketch().push([(52, -24)]).circle(33).finalize()", -19)
r=extrude(r, (-57, -16, 52), 'ZX', "sketch().arc((28, -45), (52, -57), (76, -45)).segment((68, -69)).arc((75, -85), (68, -102)).arc((52, -108), (36, -102)).arc((29, -85), (36, -69)).close().assemble().finalize()", -61)
r=extrude(r, (-34, -37, -18), 'ZX', "sketch().push([(-18, -34)]).circle(41).finalize()", -11)
r=extrude(r, (7, -44, -18), 'YZ', "sketch().push([(-44, -18)]).circle(55).finalize()", 102)
