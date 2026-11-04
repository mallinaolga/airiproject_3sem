from cadgen.extrude import extrude
r=None
r=extrude(r, (0, 0, 114), 'XY', "sketch().push([(1.5, -6)]).rect(13, 24).finalize()", -233)
r=extrude(r, (1, -6, -7), 'XY', "sketch().push([(1, -6)]).rect(20, 40).finalize()", -35, False)
r=extrude(r, (6, -18, -81), 'ZX', "sketch().push([(-81, 6)]).rect(6, 2).finalize()", -14)
r=extrude(r, (11, 2, -23), 'YZ', "sketch().push([(2, -23)]).circle(18).finalize()", 6)
r=extrude(r, (-9, -23, -38), 'YZ', "sketch().push([(-23, -38)]).circle(1).finalize()", -8)
r=extrude(r, (1, 6, -42), 'ZX', "sketch().push([(-42, 1)]).circle(1).finalize()", 6)
r=extrude(r, (-3, -25, -23), 'ZX', "sketch().segment((-40, -11), (-12, 12)).segment((-6, 5)).segment((-34, -18)).close().assemble().finalize()", -4)
r=extrude(r, (0, 6, 104), 'ZX', "sketch().segment((89, 12), (119, 21)).segment((119, -15)).segment((98, -21)).close().assemble().finalize()", 26)
