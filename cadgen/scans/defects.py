import time

import numpy as np
import open3d as o3d
import trimesh
from scipy.spatial import cKDTree

from .utils import (
    make_o3d_pc,
    multi_camera_scan,
    remove_unsupported_triangles,
)


def find_random_centers_trimesh(
    mesh: trimesh.Trimesh, radius: float, k: int = 1, seed: int | None = None
):
    """
    Выбирает k случайных центров на поверхности меша так,
    чтобы они были на расстоянии >= 2*radius друг от друга.
    """
    if seed is not None:
        np.random.seed(seed)

    # 1) сэмплируем много случайных точек с поверхности
    n_candidates = k * 50  # запас
    pts, _ = trimesh.sample.sample_surface(mesh, n_candidates)

    sel = []
    tree = None

    for p in pts:
        if not sel:
            sel.append(p)
            tree = cKDTree(np.array(sel))
        else:
            dist, _ = tree.query(p)
            if dist >= 2 * radius:
                sel.append(p)
                tree = cKDTree(np.array(sel))
                if len(sel) >= k:
                    break

    return sel[:k]


def make_hole(mesh, center, hole_radius):
    verts = mesh.vertices
    faces = mesh.faces
    face_centers = verts[faces].mean(axis=1)
    dist = np.linalg.norm(face_centers - center, axis=1)
    mask = dist > hole_radius
    mesh_with_hole = trimesh.Trimesh(vertices=verts, faces=faces[mask])
    return mesh_with_hole


def add_local_gaussian_bump(mesh, center, radius, sigma=0.2, amplitude=0.08):
    verts = mesh.vertices.copy()
    normals = mesh.vertex_normals
    dists = np.linalg.norm(verts - center, axis=1)
    mask = dists < 4 * np.sqrt(radius * sigma)
    gauss = np.exp(-0.5 * ((dists[mask] / (sigma * radius)) ** 2))
    verts[mask] += normals[mask] * (gauss * amplitude)[:, None]
    mesh_bump = trimesh.Trimesh(vertices=verts, faces=mesh.faces)
    return mesh_bump


def add_random_noise_trimesh(mesh: trimesh.Trimesh, noise_level=0.01):
    noisy_mesh = mesh.copy()
    noisy_mesh.vertices += np.random.uniform(
        -noise_level, noise_level, noisy_mesh.vertices.shape
    )
    return noisy_mesh


def make_all_defects2(
    mesh,
    n_holes=5,
    n_gaussian_holes=5,
    PC_SIZE=1000000,
    n_cameras=100,
    n_threads=1,
    log=True,
):

    start_triangles = (
        len(mesh.faces)
        if isinstance(mesh, trimesh.Trimesh)
        else len(np.asarray(mesh.triangles))
    )
    # print(start_triangles)

    timings = {}
    t_all0 = time.perf_counter()

    original_pcd = make_o3d_pc(mesh, PC_SIZE)

    t0 = time.perf_counter()
    pcds, all_points = multi_camera_scan(
        original_pcd,
        keep_scans=False,
        sin_dimension=1,
        cos_dimension=2,
        center_camera=[1, 0, 0],
        diameter=10,
        n_cameras=n_cameras,
        min_angle=-np.pi / 2,
        max_angle=np.pi / 3,
    )
    timings["сканирование"] = time.perf_counter() - t0
    if log:
        print(f"[3/7] Сканирование: {timings['сканирование']:.3f}s")

    pcd_indices = np.fromiter(all_points, dtype=np.int64)
    pcd_for_poisson = original_pcd.select_by_index(pcd_indices)

    t0 = time.perf_counter()
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd_for_poisson,
        depth=7,
        width=0,
        scale=1.1,
        linear_fit=False,
        n_threads=n_threads,
    )
    timings["восстановление_меша"] = time.perf_counter() - t0
    if log:
        print(f"[2/7] восстановление меша: {timings['восстановление_меша']:.3f}s")

    t0 = time.perf_counter()
    densities = np.asarray(densities)
    thr = np.quantile(densities, 0.10)
    mesh.remove_vertices_by_mask((densities < thr).tolist())
    timings["отсечение_низкоплотных"] = time.perf_counter() - t0
    if log:
        print(f"[5/7] Отсечение низкоплотных: {timings['отсечение_низкоплотных']:.3f}s")

    t0 = time.perf_counter()
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.remove_duplicated_vertices()
    mesh.remove_non_manifold_edges()
    mesh.remove_unreferenced_vertices()
    timings["очистка_меша"] = time.perf_counter() - t0
    if log:
        print(f"[5/7] Очистка меша: {timings['очистка_меша']:.3f}s")

    t0 = time.perf_counter()
    nn = np.asarray(pcd_for_poisson.compute_nearest_neighbor_distance())
    tau = 2.5 * nn.mean()
    mesh = remove_unsupported_triangles(mesh, pcd_for_poisson, max_dist=tau)
    mesh.compute_vertex_normals()
    timings["remove_unsupported_triangles"] = time.perf_counter() - t0
    if log:
        print(
            f"[2/7] remove_unsupported_triangles: {timings['remove_unsupported_triangles']:.3f}s"
        )

    # print("Converting to trimesh...")
    mesh = trimesh.Trimesh(
        vertices=np.asarray(mesh.vertices),
        faces=np.asarray(mesh.triangles),
        process=False,
    )

    # print("start finding centers...")

    # mesh.fill_holes()
    t0 = time.perf_counter()
    bbox = mesh.bounds
    diag = np.linalg.norm(bbox[1] - bbox[0])
    bump_radius = diag * 0.008
    hole_radius = np.random.uniform(bump_radius * 0.5, bump_radius * 1)

    n_centers = n_holes + n_gaussian_holes
    centers = find_random_centers_trimesh(
        mesh,
        radius=hole_radius,
        k=n_centers,
    )

    timings["поиск_центров"] = time.perf_counter() - t0
    if log:
        print(f"[4/7] поиск центров: {timings['поиск_центров']:.3f}s")

    t0 = time.perf_counter()
    assert (
        len(centers) == n_centers
    ), f"Only {len(centers)} centers found, needed {n_centers}"
    for i in range(n_centers):
        mesh = make_hole(mesh, center=centers[i], hole_radius=hole_radius)
        if i >= n_holes:
            mesh = add_local_gaussian_bump(
                mesh, center=centers[i], radius=bump_radius, sigma=0.8, amplitude=0.023
            )

    timings["добавление_дырок"] = time.perf_counter() - t0
    if log:
        print(f"[6/7] Добавление дырок: {timings['добавление_дырок']:.3f}s")

    mesh.fill_holes()
    mesh = add_random_noise_trimesh(mesh, noise_level=0.0001)

    t0 = time.perf_counter()
    part = 0.1
    _m = o3d.geometry.TriangleMesh()
    _m.vertices = o3d.utility.Vector3dVector(mesh.vertices)
    _m.triangles = o3d.utility.Vector3iVector(mesh.faces)
    # _m = mesh
    tri_cnt = len(np.asarray(_m.triangles))
    target = start_triangles * 5 if tri_cnt > start_triangles * 5 else tri_cnt
    _m = _m.simplify_quadric_decimation(target)
    _m.remove_degenerate_triangles()
    _m.remove_duplicated_triangles()
    _m.remove_duplicated_vertices()
    _m.remove_non_manifold_edges()
    _m.remove_unreferenced_vertices()
    _m.compute_vertex_normals()
    mesh = trimesh.Trimesh(
        vertices=np.asarray(_m.vertices), faces=np.asarray(_m.triangles), process=False
    )

    timings["упрощение_меша"] = time.perf_counter() - t0
    if log:
        print(f"[7/7] Упрощение меша: {timings['упрощение_меша']:.3f}s")

    timings["общее_время"] = time.perf_counter() - t_all0
    if log:
        print(f"  Общее время:           {timings['общее_время']:.3f}s")

    return mesh
