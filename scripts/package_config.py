from pathlib import Path


class Config:
  Root_Path = Path("../")
  Repository = "https://github.com/Caphace-Ethan/Python_USGS_LIDAR"
  Data_path = Root_Path / "data"
  Laz_path = Data_path / "laz"
  Tif_path = Data_path / "shp"
  Shp_path = Data_path / "tif"
  Image_path = Data_path / "img"
  remote_data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_FullState/ept.json"
  remote_data_directory = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"


