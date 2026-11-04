from cadgen.extrude import extrude
r=None
r=extrude(r, (0, 70, 0), 'ZX', "sketch().push([(8, 1)]).rect(40, 46).finalize()", -146)
r=extrude(r, (1, 34, 8), 'ZX', "sketch().push([(8, 1)]).rect(56, 64).finalize()", -15, False)
r=extrude(r, (-31, 25, 25), 'YZ', "sketch().arc((22, 26), (27, 27), (26, 22)).segment((26, 26)).close().assemble().finalize()", -2)
r=extrude(r, (0, 19, -19), 'ZX', "sketch().push([(-19, 0)]).circle(1).finalize()", -1)
r=extrude(r, (-22, -59, 0), 'YZ', "sketch().push([(-59, 0)]).circle(44).finalize()", -5)
r=extrude(r, (-3, 70, -10), 'ZX', "sketch().push([(-10, -3)]).rect(2, 2).finalize()", 33)
