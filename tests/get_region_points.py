import json
from numpy import fabs
# import pdal
from shapely.geometry import Polygon

from test_log import logger
import logging
import logging.handlers

import os
import sys

sys.path.append(os.path.abspath(os.path.join('./scripts')))
from package_config import Config
from FileHandler import FileHandler
from area_boundary import Boundary
from dataframe_file import Dataframe_Generator


# PUBLIC_DATA_PATH = Config.remote_data_directory
PUBLIC_DATA_PATH = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
PIPELINE_PATH = Config.test_pipeline_path


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
      pipe = self._file_handler.read_json("test_pipeline")
      print(pipe)
    except Exception as e:
      print(e)

    pipe['pipeline'][0]['filename'] = self._public_access_path + regions + "/ept.json"
    # pipe['pipeline'][0]['filename'] = self._public_access_path
    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][1]['polygon'] = polygon_str
    pipe['pipeline'][4]['out_srs'] = f'EPSG:{self.output_epsg}'
    pipe['pipeline'][5]['filename'] = str(Config.test_Laz_path / str(filename + ".laz"))
    pipe['pipeline'][6]['filename'] = str(Config.test_Tif_path / str(filename + ".tif"))
    return pdal.Pipeline(json.dumps(pipe))

  def check_cache(self):
    pass

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

    filename = region + "_" + bounds.get_boundary_name()
    print(">>>file", filename, "get_boundary_str()", bounds.get_boundary_str(), "polygon_str", polygon_str, "region", region)
    pl = self.get_pipeline(bounds.get_boundary_str(), polygon_str, region, filename)
    print(">>>pl", pl)
    try:
      pl.execute()
      geo_data = self._df_generator.get_geo_data(pl.arrays)
      self._logger.info(f"successfully read geo data: {filename}")
      return geo_data
    except RuntimeError as e:
      self._logger.exception(f"error reading geo data, error: {e}")

  def get_data(self, polygon: Polygon, regions=[]) -> None:

    bound, polygon_str = self._df_generator.get_bound_from_polygon(polygon)
    print("here1")
    if len(regions) == 0:
      regions = self.get_bound_metadata(bound)
      print("here2")
    else:
      regions = self._metadata[self._metadata['filename'].isin(regions)]
      print("here3")
      print(regions)
      if self.check_valid_bound(bound, regions) is False:
        self._logger.exception("The boundary is not within the region provided")
    print("here")
    list_geo_data = []
    for index, row in regions.iterrows():
      print(">>>", bound, polygon_str, ":::", row['filename'])
      data = self.get_geo_data(bound, polygon_str, row['filename'])
      print(">>>", data)
      list_geo_data.append({'year': row['year'],
                            'region': row['region'],
                            'geo_data': data,
                            })
    return list_geo_data


# Test
if __name__ == "__main__":
  fetcher = GetData(epsg=4326, metadata_filename="usgs3dep_region_names")
  MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]

  polygon = Polygon(((MINX, MINY), (MINX, MAXY),
                     (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))
  print(polygon)
  fetcher.get_data(polygon, ["IA_FullState"])
  # print(fetcher.get_data(polygon, ["IA_FullState"]))