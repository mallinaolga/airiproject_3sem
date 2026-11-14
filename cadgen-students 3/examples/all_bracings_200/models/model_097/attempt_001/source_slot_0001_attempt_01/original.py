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
r=extrude(r, (0, -73, 0), 'ZX', "sketch().push([(-23, -29)]).circle(48).finalize()", 168)
r=extrude(r, (-29, -38, -23), 'ZX', "sketch().push([(-23, -29)]).circle(80).finalize()", 51, False)
r=extrude(r, (51, -17, -23), 'YZ', "sketch().segment((-40, -29), (-17, 0)).segment((6, -17)).segment((-17, -46)).close().assemble().finalize()", 43)
r=extrude(r, (-95, 13, -47), 'ZX', "sketch().segment((-49, -100), (-49, -98)).arc((-50, -95), (-49, -92)).segment((-49, -90)).segment((-45, -90)).segment((-45, -92)).arc((-44, -95), (-45, -98)).segment((-45, -100)).close().assemble().finalize()", 35)
r=extrude(r, (26, 13, 26), 'ZX', "sketch().push([(26, 26)]).circle(15).finalize()", 15)
r=extrude(r, (94, -22, -40), 'YZ', "sketch().push([(-22, -40)]).rect(148, 26).push([(-28, -39)]).circle(4, mode='s').finalize()", 15)
r=extrude(r, (-86, -38, 30), 'ZX', "sketch().push([(30, -86)]).circle(13).finalize()", -30)
r=extrude(r, (-29, -7, 57), 'ZX', "sketch().arc((53, -49), (57, -29), (53, -9)).segment((69, -15)).arc((83, -9), (97, -15)).arc((103, -29), (97, -43)).arc((83, -49), (69, -43)).close().assemble().finalize()", -40)
