from cadgen.extrude import extrude
r=None
r=extrude(r, (0, 0, 44), 'XY', "sketch().push([(0, -32)]).circle(8).finalize()", -69)
r=extrude(r, (0, -32, 30), 'XY', "sketch().push([(0, -32)]).circle(9).finalize()", -7, False)
r=extrude(r, (0, -24, 40), 'ZX', "sketch().segment((11, 66), (17, 69)).segment((69, -66)).segment((63, -69)).close().assemble().finalize()", 115)
r=extrude(r, (0, -40, 0), 'ZX', "sketch().segment((-112, -54), (-112, 54)).segment((-15, 54)).segment((-15, 101)).segment((15, 101)).segment((15, 54)).segment((112, 54)).segment((112, -54)).segment((15, -54)).segment((15, -101)).segment((-15, -101)).segment((-15, -54)).close().assemble().finalize()", -51)
