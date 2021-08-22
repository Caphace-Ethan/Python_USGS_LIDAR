# USGS_LIDAR_PACKAGE

**Table of content**

- [Project Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Data](#data)
- [Package_Scripts](#pacakage_scripts)
- [Package](#package)


## Overview
Python module interfaced with USGS 3DEP, that will be used by Data Scientists to fetch, visualize, and transform publicly available satellite and LIDAR data


## Requirements
The project requires Python 3.6+, and python packages listed in `requirements.txt` file

## Installation 

1. Creating conda virtual environment [in Linux]
```
conda create -n geo_env
conda activate geo_env
conda config  --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install geopandas
conda install PDAL
```

2. Cloning the repo and install the dependency packages using `requirements.txt`
```
git clone https://github.com/Caphace-Ethan/Python_USGS_LIDAR
cd Python_USGS_LIDAR
conda install -r requirements.txt
```

## Data

- The USGS 3D Elevation Program (3DEP) provides access to lidar point cloud data from the 3DEP repository. The adoption of cloud storage and computing by 3DEP allows users to work with massive datasets of lidar point cloud data without having to download them to local machines.
- The point cloud data is freely accessible from AWS in EPT format. Entwine Point Tile (EPT) is a simple and flexible octree-based storage format for point cloud data. The organization of an EPT dataset contains JSON metadata portions as well as binary point data. The JSON file is core metadata required to interpret the contents of an EPT dataset.


## Package_Scripts
Package Scripts are found in ```scripts``` directory, its content is explained below.
- ```area_boundary:``` script for processing boundary coordinates/points of a given region.
- ```dataframe_file:``` Processing of dataframe both geo-data and normal dataframes.
- ```FileHandler:``` Helper class for reading and writing different file formats.
- ```get_usgs_region_data:``` Script for creating metadata describing the boundary points for regions.
- ```package_config: ```Script for handling package configurations such as location of files and url(s), etc.
- ```log: ```script for logging package logs

## Package

This package interacts with USGS 3DEP data through public API to retrieve data, in which for this case, the data source used is AWS



