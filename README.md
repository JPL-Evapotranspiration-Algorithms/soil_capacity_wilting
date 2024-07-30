# `soil-capacity-wilting` Python Package

The `soil_grids` Python package generates rasters of field capacity and wilting point from the [SoilGrids](https://soilgrids.org/) dataset as inputs to the [PT-JPL-SM](https://github.com/JPL-Evapotranspiration-Algorithms/PT-JPL-SM) evapotranspiration model.

[Gregory H. Halverson](https://github.com/gregory-halverson-jpl) (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
NASA Jet Propulsion Laboratory 329G

## Installation

This package is available on PyPi as a [pip package](https://pypi.org/project/soil-capacity-wilting/) called `soil-capacity-wilting` with dashes.

```bash
pip install soil-capacity-wilting
```

## Usage

Import this package as `soil_capacity_wilting` with under-scores.

```python
import soil_capacity_wilting
```

## References

Hengl T, Mendes de Jesus J, Heuvelink GBM, Ruiperez Gonzalez M, Kilibarda M, Blagotić A, et al. (2017) SoilGrids250m: Global gridded soil information based on machine learning. PLoS ONE 12 (2): e0169748.
