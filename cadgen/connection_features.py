#поиск геометрических элементов, с помощью которых детали могут соединяться друг с другом



import argparse
import json
import math
from pathlib import Path
import cadquery as cq

from .geometry_analysis import find_step_files, load_part


def vector_to_list(vector):
    return [vector.x, vector.y, vector.z]


def detect_planar_features(shape):
    features = []

    for face_id, face in enumerate(shape.Faces()):
        if face.geomType() != "PLANE":
            continue

        center = face.Center()
        normal = face.normalAt()

        features.append({
            "face_id": face_id,
            "type": "planar",
            "area": face.Area(),
            "center": vector_to_list(center),
            "normal": vector_to_list(normal),
        })

    return features



def detect_cylindrical_features(shape):
    """Определяет цилиндрические поверхности и их предварительный тип."""
    features = []

    bbox = shape.BoundingBox()
    scale = max(bbox.xlen, bbox.ylen, bbox.zlen, 1.0)
    epsilon = max(scale * 1e-5, 1e-5)

    for face_id, face in enumerate(shape.Faces()):
        if face.geomType() != "CYLINDER":
            continue

        cylinder = face._geomAdaptor().Cylinder()
        axis = cylinder.Axis()
        direction = axis.Direction()
        location = axis.Location()

        radius = float(cylinder.Radius())

        # Нормаль берём в точке внутри цилиндрической грани.
        point = face.Center()
        normal = face.normalAt().normalized()

        # Проекция точки на ось цилиндра.
        axis_point = cq.Vector(
            location.X(), location.Y(), location.Z()
        )
        axis_direction = cq.Vector(
            direction.X(), direction.Y(), direction.Z()
        ).normalized()

        along_axis = (point - axis_point).dot(axis_direction)
        nearest_axis_point = axis_point + axis_direction * along_axis

        radial = point - nearest_axis_point

        role = "unknown"

        if radial.Length > epsilon:
            radial_direction = radial.normalized()
            dot = normal.dot(radial_direction)

            # На наружной цилиндрической поверхности
            # нормаль направлена от оси.
            if dot > 0.9:
                role = "outer"

            # На стенке отверстия нормаль направлена к оси.
            elif dot < -0.9:
                role = "inner"

        features.append({
            "face_id": face_id,
            "type": "cylindrical",
            "radius": radius,
            "diameter": 2.0 * radius,
            "axis_point": [
                location.X(), location.Y(), location.Z()
            ],
            "axis_direction": [
                direction.X(), direction.Y(), direction.Z()
            ],
            "area": float(face.Area()),
            "role": role,
        })

    return features


def faces_share_edge(face_a, face_b):
    for edge_a in face_a.Edges():
        for edge_b in face_b.Edges():
            if edge_a.isSame(edge_b):
                return True

    return False


def calculate_angle(normal_a, normal_b):
    dot = (
        normal_a.x * normal_b.x
        + normal_a.y * normal_b.y
        + normal_a.z * normal_b.z
    )

    dot = max(-1.0, min(1.0, dot))

    angle = math.degrees(math.acos(abs(dot)))

    return angle


def classify_edge(shape, face_a, face_b):
    shared_edge = None

    for edge_a in face_a.Edges():
        for edge_b in face_b.Edges():
            if edge_a.isSame(edge_b):
                shared_edge = edge_a
                break
        if shared_edge is not None:
            break

    if shared_edge is None:
        return "unknown"

    normal_a = face_a.normalAt().normalized()
    normal_b = face_b.normalAt().normalized()

    direction = normal_a - normal_b

    if direction.Length < 1e-10:
        return "unknown"

    direction = direction.normalized()

    bbox = shape.BoundingBox()
    dimensions = [bbox.xlen, bbox.ylen, bbox.zlen]
    dimensions = [d for d in dimensions if d > 0]

    if not dimensions:
        return "unknown"

    epsilon = max(1e-5, min(dimensions) * 1e-4)

    midpoint = shared_edge.positionAt(0.5)

    point_a = midpoint + direction * epsilon
    point_b = midpoint - direction * epsilon

    tolerance = epsilon * 0.01

    inside_a = shape.isInside(point_a, tolerance)
    inside_b = shape.isInside(point_b, tolerance)

    if inside_a and inside_b:
        return "concave"

    if not inside_a and not inside_b:
        return "convex"

    return "unknown"



def find_adjacent_planar_faces(shape):
    faces = shape.Faces()

    planar_faces = {
        i: face
        for i, face in enumerate(faces)
        if face.geomType() == "PLANE"
    }

    edge_to_faces = {}

    for face_id, face in planar_faces.items():
        for edge in face.Edges():
            key = edge.hashCode()
            edge_to_faces.setdefault(key, []).append(
                (face_id, edge)
            )

    adjacent_pairs = []
    processed_pairs = set()

    for entries in edge_to_faces.values():
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                face_id_a, edge_a = entries[i]
                face_id_b, edge_b = entries[j]

                if face_id_a == face_id_b:
                    continue

                if not edge_a.isSame(edge_b):
                    continue

                pair_key = tuple(sorted((
                    face_id_a, face_id_b
                )))

                if pair_key in processed_pairs:
                    continue

                processed_pairs.add(pair_key)

                face_a = planar_faces[face_id_a]
                face_b = planar_faces[face_id_b]

                angle = calculate_angle(
                    face_a.normalAt(),
                    face_b.normalAt()
                )

                if angle <= 1.0:
                    continue

                edge_type = classify_edge(
                    shape, face_a, face_b
                )

                edge_center = edge_a.Center()

                edge_direction = None

                if edge_a.geomType() == "LINE":
                    vertices = edge_a.Vertices()

                    if len(vertices) == 2:
                        start = vertices[0].Center()
                        end = vertices[1].Center()

                        direction = end - start

                        if direction.Length > 1e-8:
                            direction = direction.normalized()

                            components = [
                                direction.x,
                                direction.y,
                                direction.z
                            ]

                            for component in components:
                                if abs(component) > 1e-8:
                                    if component < 0:
                                        components = [-v for v in components]
                                    break

                            edge_direction = components

                adjacent_pairs.append({
                    "face_ids": [face_id_a, face_id_b],
                    "angle": angle,
                    "area_a": face_a.Area(),
                    "area_b": face_b.Area(),
                    "edge_type": edge_type,
                    "edge_length": edge_a.Length(),
                    "edge_center": [
                        edge_center.x,
                        edge_center.y,
                        edge_center.z
                    ],
                    "edge_geometry": edge_a.geomType(),
                    "edge_direction": edge_direction
                })

    return adjacent_pairs


def detect_rectangular_features(shape):
    features = []

    adjacent_pairs = find_adjacent_planar_faces(shape)

    for pair in adjacent_pairs:
        if abs(pair["angle"] - 90.0) > 1.0:
            continue

        features.append({
            "type": "rectangular_candidate",
            "face_ids": pair["face_ids"],
            "angle": pair["angle"],
            "role": pair["edge_type"],
            "edge_length": pair["edge_length"],
            "edge_center": pair["edge_center"],
            "edge_geometry": pair["edge_geometry"],
            "edge_direction": pair["edge_direction"]
        })

    return features


def detect_prismatic_features(shape):
    features = []

    adjacent_pairs = find_adjacent_planar_faces(shape)

    for pair in adjacent_pairs:
        angle = pair["angle"]

        if angle <= 1.0:
            continue

        if abs(angle - 90.0) <= 1.0:
            continue

        features.append({
            "type": "prismatic_candidate",
            "face_ids": pair["face_ids"],
            "angle": pair["angle"],
            "role": pair["edge_type"],
            "edge_length": pair["edge_length"],
            "edge_center": pair["edge_center"],
            "edge_geometry": pair["edge_geometry"],
            "edge_direction": pair["edge_direction"]
        })

    return features


def extract_section_contours(section):
    contours = []

    wires = section.wires().vals()

    for wire_id, wire in enumerate(wires):
        edges = wire.Edges()

        if not wire.IsClosed():
            continue

        points = []

        for edge in edges:
            for vertex in edge.Vertices():
                point = vertex.Center()
                coordinates = [point.x, point.y, point.z]

                if not any(
                    math.dist(coordinates, existing) < 1e-6
                    for existing in points
                ):
                    points.append(coordinates)

        contours.append({
            "wire_id": wire_id,
            "edges_count": len(edges),
            "vertices_count": len(points),
            "vertices": points,
        })

    return contours


def analyze_cross_sections(shape):
    bbox = shape.BoundingBox()

    center = (
        (bbox.xmin + bbox.xmax) / 2,
        (bbox.ymin + bbox.ymax) / 2,
        (bbox.zmin + bbox.zmax) / 2
    )

    directions = {
        "X": ((0, 1, 0), (1, 0, 0)),
        "Y": ((1, 0, 0), (0, 1, 0)),
        "Z": ((1, 0, 0), (0, 0, 1))
    }

    sections = {}

    for axis, (x_dir, normal) in directions.items():
        plane = cq.Plane(
            origin=center,
            xDir=x_dir,
            normal=normal
        )

        try:
            section = (
                cq.Workplane(plane)
                .newObject([shape])
                .section()
            )

            edges = section.edges().vals()
            contours = extract_section_contours(section)

            sections[axis] = {
                "edges_count": len(edges),
                "contours_count": len(contours),
                "contours": contours,
                "edges": [
                    {
                        "length": edge.Length(),
                        "geometry": edge.geomType(),
                        "center": [
                            edge.Center().x,
                            edge.Center().y,
                            edge.Center().z
                        ]
                    }
                    for edge in edges
                ]
            }

        except Exception as error:
            sections[axis] = {
                "error": str(error)
            }

    return sections


def detect_connection_features(shape):
    return {
        "planar": detect_planar_features(shape),
        "cylindrical": detect_cylindrical_features(shape),
        "rectangular": detect_rectangular_features(shape),
        "prismatic": detect_prismatic_features(shape),
        "cross_sections": analyze_cross_sections(shape),
    }


def analyze_connections(folder, output_path):
    step_files = find_step_files(folder)

    print(f"Найдено STEP-файлов: {len(step_files)}")

    results = []

    for file_path in step_files:
        try:
            shape = load_part(file_path)

            features = detect_connection_features(shape)

            result = {
                "file": str(file_path),
                "features": features,
            }

            results.append(result)

            print(f"\nДеталь: {file_path.name}")

            for feature_type, items in features.items():
                if feature_type == "cross_sections":
                    for axis, section in items.items():
                        if "error" in section:
                            print(f"  Сечение {axis}: ошибка {section['error']}")
                        else:
                            print(
                                f"  Сечение {axis}: "
                                f"{section['edges_count']} рёбер, "
                                f"{section['contours_count']} контуров"
                            )
                else:
                    print(f"  {feature_type}: {len(items)}")

                if feature_type in ("rectangular", "prismatic"):
                    convex = sum(
                        item["role"] == "convex"
                        for item in items
                    )

                    concave = sum(
                        item["role"] == "concave"
                        for item in items
                    )

                    unknown = sum(
                        item["role"] == "unknown"
                        for item in items
                    )

                    print(f"    convex: {convex}")
                    print(f"    concave: {concave}")
                    print(f"    unknown: {unknown}")


        except Exception as error:
            print(
                f"Ошибка при анализе {file_path}: {error}"
            )

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(
        f"\nУспешно обработано деталей: {len(results)}"
    )

    print(
        f"Результаты сохранены: {output_path}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "folder",
        help="Папка со STEP-моделями",
    )

    parser.add_argument(
        "--output",
        default="connection_features.json",
        help="Путь для сохранения результатов",
    )

    args = parser.parse_args()

    analyze_connections(
        args.folder,
        args.output,
    )

