# EUDA

**E**li's **U**niaxial **D**ata **A**nalysis


---

## Project Description

### What is this?
* Research project, data analysis, & visualization


### How does this work?
* python3, data (available upon request), and libraries included in `headers.py`
* Run scripts in project folder in order


### What is the goal?
* Mechanical-Geometrical analysis of uniaxial data


### How is this organized?
1. Imports handled in `headers.py`
1. Functions are in `func.py` and `elib.py`
1. A project folder is used for each data set e.g. `p20`
1. Project folder structure:
    * `_data`
        * `raw` - raw data
        * `interm` - intermediate data storage for machine use
        * `output` - for human use, validation, logging, etc.
    1. `init` - collect and organize data
    1. `transform` - surface transforms
    1. `graph` - 3D rendering and plotting
    1. `viz` - visualization: plots, renders, etc.
1. `_snapshots` weekly local backup non-data files & show modified files
        
### License
* See `LICENSE.md` -- free to copy, use, modify, etc.

### Questions/requests
* Contact broemere
