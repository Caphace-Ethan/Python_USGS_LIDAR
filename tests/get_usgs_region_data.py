import re
import json
import urllib3
import pandas as pd
from test_log import logger
import os
import sys

sys.path.append(os.path.abspath(os.path.join('./scripts')))

from package_config import Config

from FileHandler import FileHandler

usgs_data_public_url = Config.remote_data_directory
usgs_data_filename = Config.region_names

# from clean_audio import CleanAudio
# from file_handler import FileHandler
# from audio_vis import AudioVis

class GetMetadata():

  def __init__(self, name: str = usgs_data_filename, target_url: str = usgs_data_public_url):
    self.url = target_url
    self.filename = name
    self._http = urllib3.PoolManager()
    self._file_handler = FileHandler()
    self._logger = logger("GetMetadata")

  def get_name_and_year2(self, filename):
    filename = filename.replace('/', '')
    regex = '20[0-9][0-9]+'
    match = re.search(regex, filename)
    if match:
      return filename[:match.start() - 1], filename[match.start():match.end()]
    else:
      return filename, None

  def get_metadata(self):
    filenames = self._file_handler.read_txt(self.filename)
    df = pd.DataFrame(columns=['filename', 'region', 'year', 'xmin', 'xmax', 'ymin', 'ymax', 'points'])

    index = 0
    for f in filenames:
      r = self._http.request('GET', self.url + f + "ept.json")
      if r.status == 200:
        j = json.loads(r.data)
        region, year = self.get_name_and_year2(f)

        df = df.append({
          'filename': f.replace('/', ''),
          'region': region,
          'year': year,
          'xmin': j['bounds'][0],
          'xmax': j['bounds'][3],
          'ymin': j['bounds'][1],
          'ymax': j['bounds'][4],
          'points': j['points']}, ignore_index=True)

        if(index % 100 == 0):
          print(f"Read progress: {((index / len(filenames)) * 100):.2f}%")
        index += 1
      else:
        self._logger.exception(f"Connection problem at: {f}")
        # return
    self._file_handler.save_csv(df, usgs_data_filename)


if __name__ == "__main__":
  gm = GetMetadata()
  gm.get_metadata()