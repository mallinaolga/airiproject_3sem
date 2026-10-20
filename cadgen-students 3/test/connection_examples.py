"""Create viewable examples: python test/connection_examples.py"""

from datetime import datetime
from pathlib import Path

import cadquery as cq

from cadgen.assembly_search import run_search
from cadgen.connection_search import SearchSettings


def corner_and_cube():
    corner = (cq.Workplane("XY")
              .polyline([(0, 0), (30, 0), (30, 4), (4, 4), (4, 30), (0, 30)])
              .close().extrude(12).val())
    cube = cq.Workplane("XY").box(10, 10, 10).val()
    return corner, cube


def oval_and_recess():
    oval = cq.Workplane("XY").sphere(1).val().transformGeometry(
        cq.Matrix([[10, 0, 0, 0], [0, 7, 0, 0], [0, 0, 5, 8], [0, 0, 0, 1]]))
    block = cq.Workplane("XY").box(30, 25, 7, centered=(True, True, False)).val()
    return block.cut(oval), oval


def main():
    root = Path(__file__).resolve().parent / (
        "contact_examples_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    for name, shapes in (("corner_cube", corner_and_cube()),
                         ("oval_recess", oval_and_recess())):
        folder = root / name / "parts"
        folder.mkdir(parents=True)
        for index, shape in enumerate(shapes):
            # Deliberately separate the initial models; the search must find the pose.
            if index:
                shape = shape.rotate((0, 0, 0), (1, 2, 3), 23).translate((80, 20, 40))
            for extension in ("step", "stl"):
                cq.exporters.export(shape, str(folder / f"{index}.{extension}"))
        report = run_search(folder, root / name / "connections", SearchSettings())
        if report["summary"]["assemblies_exported"] != 1:
            raise RuntimeError(f"Example failed: {name}; see its report.json")
    print(f"\nView examples under: {root}")


if __name__ == "__main__":
    main()
