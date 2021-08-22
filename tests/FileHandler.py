import json
import laspy
import pandas as pd
from test_log import logger
import logging
import logging.handlers

import os
import sys

sys.path.append(os.path.abspath(os.path.join('./scripts')))
from package_config import Config

class FileHandler():

  def __init__(self):
    self._logger = logging

  def save_csv(self, df, name, index=False):
    try:
      path = Config.Test_data_path / str(name + '.csv')
      df.to_csv(path, index=index)
      self._logger.info(f"{name} file saved successfully in csv format")
    except Exception:
      self._logger.exception(f"{name} save failed")

  def read_csv(self, name, missing_values=[]):
    try:
      path = Config.Test_data_path / str(name + '.csv')
      df = pd.read_csv(path, na_values=missing_values)
      self._logger.info(f"{name} file read successfully")
      return df
    except FileNotFoundError:
      self._logger.exception(f"{name} not found")

  def read_json(self, name):
    try:
      path = Config.Test_data_path / str(name + '.json')
      # print("FileHandlerv-pipeline >>", path)   # For Debugging purposes
      with open(path, 'r') as json_file:
        json_obj = json.load(json_file)
      self._logger.info(f"{name} file read successfully")
      return json_obj
    except Exception:
      self._logger.exception(f"{name} not found")

  def read_txt(self, name):
    try:
      path = Config.Data_path / str(name + '.txt')
      with open(path, "r") as f:
        text_file = f.read().splitlines()
      self._logger.info(f"{name} file read successfully")
      return text_file
    except Exception:
      self._logger.exception(f"{name} not found")

  def read_point_data(self, name) -> dict:
    try:
      path = Config.test_Laz_path / str(name + '.laz')
      print(path)
      las = laspy.read(path)
      self._logger.info(f"{name} read successfully")
      return las
    except Exception:
      self._logger.exception(f"{name} not found")