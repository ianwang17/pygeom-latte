# Welcome to pygeomlatte's documentation!

Python package containing the Monte Carlo geometry implementation of the LEGEND
HPGe characterization test stand LATTE.

This geometry can be used as an input to the
[remage](https://remage.readthedocs.io/en/stable/) simulation software.

This package is based on {doc}`pyg4ometry <pyg4ometry:index>`,
{doc}`legend-pygeom-hpges <legendhpges:index>` (implementation of HPGe
detectors), {doc}`legend-pygeom-l1000 <legend1000:index>` (implementation of HPGe
detector holders and optical materials) and {doc}`legend-pygeom-tools <pygeomtools:index>`.

## Installation

The latest tagged version and all its dependencies can be installed from PyPI:
`pip install pygeom-latte`.

Alternatively, the packages's development version can be installed from a git
checkout: `pip install -e .` (in the directory of the git checkout).

:::{important}
This package relies on `legend-pygeom-tools` and `legend-pygeom-l1000` to run. Stable releases are available on conda-forge. See [remage](https://remage.readthedocs.io/en/stable/) installation instructions for walk-through instructions to set up an appropriate virtual environment or container.  
:::

## Command Line Interface
After installation, the Command Line Interface utility `pygeom-latte` is provided on your `$PATH`. This CLI utility is the primary way to interact with this package. It requires a config file (example provided as `sample.yaml`) and produces an output GDML geometry file. You can find usage docs by running `pygeom-latte -h`. 
In the simplest case, you can run it by running the terminal command:

```
$ pygeom-latte --config sample.yaml mygeometry.gdml
```


```{toctree}
:maxdepth: 1
:caption: Development

Package API reference <api/modules>

