# pdal pipeline <name of pipeline> --debug
# https://s3-us-west-2.amazonaws.com/usgs-lidar-public/RegioName/ept.json Using PDAL pipeline

# MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]
# polygon = Polygon(((MINX, MINY), (MINX, MAXY), (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))

import json
from numpy import fabs
import pdal
from shapely.geometry import Polygon

import logging
import logging.handlers

import os
import sys

sys.path.append(os.path.abspath(os.path.join('scripts')))
from package_config import Config
from area_boundary import Boundary
from FileHandler import FileHandler
from dataframe_file import Dataframe_Generator
from log import logger


PUBLIC_DATA_PATH = Config.remote_data_directory
PIPELINE_PATH = Config.pipeline_path


class GetData:
  def __init__(self,
               epsg=26915,
               public_access_path: str = PUBLIC_DATA_PATH,
               metadata_filename: str = "",
               ):
    self._input_epsg = 3857
    self.output_epsg = epsg
    self._public_access_path = public_access_path
    self._df_generator = Dataframe_Generator(self._input_epsg, self.output_epsg)
    self._file_handler = FileHandler()
    self._logger = logger("GetData")
    self._logger = logging
    self._metadata = self._file_handler.read_csv(metadata_filename)

  def get_pipeline(self, bounds, polygon_str, regions, filename):
    try:
      pipe = self._file_handler.read_json("pipeline")
      print("Successfully read pipeline json file")
    except Exception as e:
      print(e)
      print("Reading json failed")

    pipe['pipeline'][0]['filename'] = self._public_access_path + regions + "/ept.json"
    # pipe['pipeline'][0]['filename'] = self._public_access_path
    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][1]['polygon'] = polygon_str
    pipe['pipeline'][4]['out_srs'] = f'EPSG:{self.output_epsg}'
    pipe['pipeline'][5]['filename'] = str(Config.Laz_path / str(filename + ".laz"))
    pipe['pipeline'][6]['filename'] = str(Config.Shp_path / str(filename + ".shp"))
    return pdal.Pipeline(json.dumps(pipe))


  def get_bound_metadata(self, bounds: Boundary):

    filtered_df = self._metadata.loc[
      (self._metadata['xmin'] <= bounds.xmin)
      & (self._metadata['xmax'] >= bounds.xmax)
      & (self._metadata['ymin'] <= bounds.ymin)
      & (self._metadata['ymax'] >= bounds.ymax)
    ]
    return filtered_df[["filename", "region", "year"]]

  def check_valid_bound(self, bounds: Boundary, regions):
    for index, row in regions.iterrows():
      cond = (row['xmin'] <= bounds.xmin) & (row['xmax'] >= bounds.xmax) & (row['ymin'] <= bounds.ymin) & (row['ymax'] >= bounds.ymax)
      if cond is False:
        return False

    return True

  def get_geo_data(self, bounds: Boundary, polygon_str, region) -> None:

    # filename = region + "_" + bounds.get_boundary_name()
    filename = "iowa"
    pl = self.get_pipeline(bounds.get_boundary_str(), polygon_str, region, filename)
    try:
      pl.execute()
      self._logger.info("pl execution successfully>>")
      geo_data = self._df_generator.get_geo_data(pl.arrays)
      self._logger.info(f"successfully read geo data: {filename}")
      self._logger.info(f"Geo Data: {geo_data}")
      return geo_data
    except RuntimeError as e:
      self._logger.exception(f"error reading geo data, error: {e}")

  def get_data(self, polygon: Polygon, regions=[]) -> None:

    bound, polygon_str = self._df_generator.get_bound_from_polygon(polygon)

    if len(regions) == 0:
      regions = self.get_bound_metadata(bound)

    else:
      regions = self._metadata[self._metadata['filename'].isin(regions)]
      if self.check_valid_bound(bound, regions) is False:
        self._logger.exception("The boundary is not within the region provided")

    list_geo_data = []
    for index, row in regions.iterrows():
      data = self.get_geo_data(bound, polygon_str, row['filename'])
      list_geo_data.append({'year': row['year'],
                            'region': row['region'],
                            'geo_data': data,
                            })
    return list_geo_data


# Testing the functions
# if __name__ == "__main__":
#   fetcher = GetData(epsg=4326, metadata_filename="usgs3dep_region_data")
#   MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]
#
#   polygon = Polygon(((MINX, MINY), (MINX, MAXY),
#                      (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
#   # print(polygon)
#   print(fetcher.get_data(polygon, ["IA_FullState"]))
