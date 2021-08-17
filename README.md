# Python_USGS_LIDAR

**Table of content**

- [Project Overview](##overview)
- [Requirements](##requirements)
- [Installation](##installation)
- [To be added](##tobeadded)

## Overview
Python module interfaced with USGS 3DEP, that will be used by Data Scientists to fetch, visualize, and transform publicly available satellite and LIDAR data


## Requirements
The project requires Python 3.6+, and python packages listed in `requirements.txt` file

## Installation 

1. Creating conda virtual environment [in ubuntu]
```
conda create -n geo_env
conda activate geo_env
conda config  --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install geopandas
```

2. Cloning the repo and install the dependency packages using `requirements.txt`
```
git clone https://github.com/Caphace-Ethan/Python_USGS_LIDAR
cd Python_USGS_LIDAR
pip install -r requirements.txt
```

## tobeadded