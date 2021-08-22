import geopandas as gpd
from shapely.geometry import Polygon, Point
import json, ast
from os import stat

import logging
import logging.handlers
from test_log import logger

def crs_to_epsg(list):

	s = gpd.GeoSeries([Point(list[0], list[1]), Point(list[2], list[3])])

	s.set_crs(epsg=4326, inplace=True)
	s = s.to_crs(epsg=3857)
	print(s)
	logger("test_logs")
	return s

list = [-93.756155, 41.918015, -93.747334, 41.921429]

bounds = crs_to_epsg(list)