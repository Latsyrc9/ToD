#!/usr/bin/env python
import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

from tools.data_transformation import FileDataTransformation as fdt

sample_file = fdt('sample.csv')
df_data = sample_file.get_df()
print(df_data)

settings_file = fdt('settings.json')
settings_data = settings_file.get_json_obj()
print(settings_file.get_json_obj_as_str())

custom_settings_file = fdt('custom_settings.json')
custom_settings_file.set_value('Starting Lvl',0)
print(custom_settings_file.get_json_obj_as_str())
