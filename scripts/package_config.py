from pathlib import Path


class Config:

  Root_Path = Path("./")
  Repository = "https://github.com/Caphace-Ethan/Python_USGS_LIDAR"
  Data_path = Root_Path / "data"
  Laz_path = Data_path / "laz"
  Tif_path = Data_path / "tif"
  Shp_path = Data_path / "shp"
  Image_path = Data_path / "img"

  Test_data_path = Root_Path / "tests/test_data"
  test_Laz_path = Test_data_path / "laz"
  test_Tif_path = Test_data_path / "tif"
  test_Shp_path = Test_data_path / "shp"
  test_Image_path = Test_data_path / "img"

  remote_data_path = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/IA_FullState/ept.json"
  remote_data_directory = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
  region_names = "usgs3dep_region_data"

  pipeline_path = Root_Path / "data/pipeline.json"
  test_pipeline_path = Root_Path / "tests/test_pipeline.json"



