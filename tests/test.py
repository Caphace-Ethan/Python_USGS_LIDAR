import geopandas as gpd
from shapely.geometry import Polygon, Point
import json, ast
from os import stat


s = gpd.GeoSeries([Point(-93.756155, 41.918015), Point(-93.747334, 41.921429)])

s.set_crs(epsg=4326, inplace=True)
s = s.to_crs(epsg=3857)
print(s)

