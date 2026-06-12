# Welcome to pygeomlatte's documentation!

Python package containing the Monte Carlo geometry implementation of the LEGEND
HPGe characterization test stand LATTE.

This geometry can be used as an input to the
[remage](https://remage.readthedocs.io/en/stable/) simulation software.

This package is based on {doc}`pyg4ometry <pyg4ometry:index>`,
{doc}`legend-pygeom-hpges <legendhpges:index>` (implementation of HPGe
detectors) and {doc}`legend-pygeom-tools <pygeomtools:index>`.

## Installation

:::{important}

For using all its features, this package requires a working setup of
[`legend-metadata`](https://github.com/legend-exp/legend-metadata) (_private
repository_) before usage. A limited public geometry is also implemented.

:::

The latest tagged version and all its dependencies can be installed from PyPI:
`pip install pygeom-latte`.

Alternatively, the packages's development version can be installed from a git
checkout: `pip install -e .` (in the directory of the git checkout).

```{toctree}
:maxdepth: 1
:caption: Development

Package API reference <api/modules>

