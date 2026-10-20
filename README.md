# CADGen — student distribution

Generate CAD programs and STL meshes using public Python dependencies.
No access to the original GitLab repositories is needed for procedural generation.

## Install

Extract the archive, then open a terminal in the `cadgen-students` folder.
Use Python 3.11 and an isolated environment. For example, with Conda:

```bash
conda create -n cadgen python=3.11 -y
conda activate cadgen
python -m pip install -e .
cadgen --help
```

Alternatively, create a virtual environment with `python3.11 -m venv .venv`,
activate it, and run the same pip command. Internet access is needed to download
the public Python packages. Keep this extracted folder after editable installation.

## Generate a small dataset

Run from this folder:

```bash
cadgen gen --output ./generations/demo --n-train-samples 10 --n-val-samples 0 --n-folders 1 --max-workers 1
```

Programs and meshes are written below `generations/demo/train/`, with a
`train.pkl` index at `generations/demo/`. Generation may retry unsuccessful
random shapes. Specify the sample count: the original CLI default is one million.

## Choose operations

For lofts:

```bash
cadgen gen --output ./generations/loft --cad-factory-config configs/operations/loft.py --n-train-samples 10 --n-val-samples 0 --n-folders 1 --max-workers 1
```

For combined operations:

```bash
cadgen gen --output ./generations/combined --cad-factory-config configs/datasets/py_configs/eo_loft_sweepadv.py --n-train-samples 10 --n-val-samples 0 --n-folders 1 --max-workers 1
```

More Python presets are in `configs/operations/` and
`configs/datasets/py_configs/`. Each exposes a `cad_factory` object.

## What changed for this distribution

- The four GitLab installation dependencies were removed. Core dependencies
  are declared explicitly in `pyproject.toml`.
- Imports used only by metadata, rendering, statistics, or external SketchGraphs
  sampling are deferred until those features are explicitly requested.
- Automatic collage rendering is off. Geometry generation, validation, and
  Python/STL output remain enabled.
- The small `attach_at` and `circular_pattern` CadQuery extensions are bundled
  under `cadgen/_addons/`, derived from the local `cadquery_addons` package by
  Daniel Ignatyev. They use the selectors already included in CADGen.
- Generated programs import both edge and face selectors explicitly so they can
  execute independently of the original add-on package.

Procedural generation does not need `cadlib`, `cq_parser`, `sg_parser`, `cadaxt`,
or `cadquery_addons`. Optional CoT metadata (`--use-cot-filter`), legacy parser
helpers, collage rendering, external statistics, and SketchGraphs sampling still
require their original libraries/data if you choose to use them. Keep these
features disabled for this self-contained generator distribution.

Mesh defects are optional and require the public extra
`python -m pip install -e ".[defects]"` before using `--with-defects`.

The original YAML presets are retained for reference/customization. Some use
server paths, legacy factory settings, or external SketchGraphs data. Start with
the CLI or Python presets above. For procedural sketches, use
`from_sketchgraph=False` and no positive `from_sketchgraph_probability`.

## More options

```bash
cadgen gen --help
```

Programmatic generation is available through `cadgen.cli.CADGenCli.generate`.
Put calls inside `if __name__ == "__main__":` when using scripts because the
generator starts worker processes.

This archive excludes generated datasets, notebooks, test fixtures, renders,
development notes, cluster scripts, and caches.

## Verification

Verified on macOS with Python 3.11 and public CadQuery 2.5.2 in a fresh virtual
environment containing none of the private libraries. Installation and
`pip check` passed. The CLI generated three training samples and one validation
sample, with Python/STL pairs and valid indexes; exported meshes were watertight
and had positive volume. Separate geometry checks passed for the default
factory, extrude, loft, revolve, array patterns, surface attachment, and circular
patterns with private-library imports explicitly blocked. Other platforms and
all optional presets were not exhaustively tested.
