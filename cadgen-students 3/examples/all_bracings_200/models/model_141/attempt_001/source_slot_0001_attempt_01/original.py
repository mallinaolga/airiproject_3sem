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
r=extrude(r, (48, 0, 0), 'YZ', "sketch().push([(10.5, 1.5)]).rect(11, 73).finalize()", -156)
r=extrude(r, (-84, 11, 2), 'YZ', "sketch().push([(11, 2)]).rect(14, 96).finalize()", -23, False)
r=extrude(r, (3, 16, 19), 'YZ', "sketch().push([(-17.5, 19)]).rect(67, 46).finalize()", 86)
r=extrude(r, (89, -23, 5), 'YZ', "sketch().segment((-44, 13), (-11, 24)).segment((-2, -3)).segment((-35, -14)).close().assemble().finalize()", 5)
r=extrude(r, (49, 8, 43), 'XY', "sketch().push([(49, 8)]).circle(46).finalize()", 12)
r=extrude(r, (47, 43, 55), 'ZX', "sketch().push([(-7, 47)]).rect(124, 120).finalize()", -2)
r=extrude(r, (33, -51, 0), 'ZX', "sketch().push([(0, 33)]).rect(138, 74).finalize()", -3)
r=extrude(r, (-30, 5, -15), 'XY', "sketch().segment((-44, 5), (-40, 12)).arc((-44, 23), (-40, 33)).arc((-30, 37), (-20, 33)).arc((-16, 23), (-20, 12)).segment((-16, 5)).close().assemble().push([(-30, 23)]).circle(5, mode='s').finalize()", 29)
