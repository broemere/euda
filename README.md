<!-- PROJECT LOGO -->
<br />
<div align="center">
	<a target="_blank" rel="noopener noreferrer" href="https://github.com/broemere/euda">
		<img src="https://raw.githubusercontent.com/broemere/euda/master/euda-header.png">
	</a>
    <p>
        <a href="#installation">Installation</a> •
        <a href="#usage">Usage</a> •
        <a href="#features">Features</a> •
        <a href="#roadmap">Roadmap</a> •
        <a href="#license">License</a>
    </p>
</div>

---

This is a research tool for processing and visualizing data 
collected from biological tissue stretch experiments.

It is intended to be used with raw data by
running the scripts in order--jupyter notebook style.

The work here is primarily for soft tissue mechanical 
analysis and has bio-mechanical assumptions built in. 
However it could be easily adapted for non-biological 
materials.

# Installation

Requires ```python3 64-bit```

Developed on <a href="https://www.python.org/downloads/release/python-3913/">python v3.9.13</a>

### Package Requirements

* matplotlib
* numpy
* pandas
* scipy
* opencv-python
* mayavi

```
pip install -r requirements.txt
```

# Usage

### Examples

Uniaxial test recording (raw video data): 

<p>
&nbsp;&nbsp;&nbsp;&nbsp;
<a href="https://github.com/broemere/euda/raw/master/src/p20/examples/13D_ring_test.avi">
src\p20\examples\13D_ring_test.avi
</a>
</p>

Autothresholding example

```
python src\p20\examples\auto-thresh-example.py
```

### Organization

1. Imports handled in `headers.py`
1. Functions are in `func.py` and `elib.py`
1. A project folder is used for each data set e.g. `p20`
1. Project folder structure:
    * `_data`
        * `raw` - raw data
        * `interm` - intermediate data storage for machine use
        * `output` - for human use, validation, logging, etc.
    1. `init` - collect and organize data
    1. `transform` - data transforms
    1. `graph` - 3D rendering and plotting
    1. `viz` - visualization: plots, renders, etc.
1. `_snapshots` weekly local backup of code & modified files shown


# Features

* Import and clean video and .csv data
* Auto-threshold samples from video
    * Goal seek minimum RMSE and maximum stretch ( &lambda; )
* Geometric modeling
    * Voxel 3D reconstruction of sample
* Mechanical modeling
    * Sample material stress and stretch

# Roadmap

- [x] Model mechanical stress
- [x] 3D visualizer
- [ ] Create failure stress graph

# License

Distributed under the MIT License. See ```LICENSE.txt``` for more information.

# Contact

broemere