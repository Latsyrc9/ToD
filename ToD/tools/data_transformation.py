#!/usr/bin/env python
import os
import json
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))

class FileDataTransformation():

    def __init__(self, filename):
        '''Name of file in the data folder'''
        self.file_path = dir_path + '/../data/' + filename
        if filename.endswith('.csv'):
            self._file_to_dataframe()
        elif filename.endswith('.json'):
            self._file_to_json_obj()

    def get_file_path(self):
        '''File path'''
        return self.file_path

    def get_json_obj_as_str(self):
        '''Return JSON object as string'''
        person_string = json.dumps(self.json_data, indent = 4, sort_keys=True)
        return person_string
    
    def get_json_obj(self):
        return self.json_data

    def get_df(self):
        return self.df_data

    def set_json_file(self):
        '''Update JSON file'''
        with open(self.file_path, 'w') as self.file_path:
            json.dump(self.json_data, self.file_path, indent = 4, sort_keys=True)

    def set_value(self, value, data):
        '''Update Value {value:data}'''
        self.json_data[value] = data
        return True

    def _file_to_dataframe(self):
        '''Converts file to Dataframe'''
        self.df_data = pd.read_csv(self.file_path)
        return self.df_data

    def _file_to_json_obj(self):
        '''Converts file to JSON object'''
        with open(self.file_path) as f:
            self.json_data = json.load(f)
        return self.json_data

    # Cutome data conversion
    def dict_to_json_file(self, person_dict):
        '''Convets dictionay to JSON file'''
        with open(self.file_path, 'w') as json_file:
            json.dump(person_dict, json_file, indent = 4, sort_keys=True)

    def json_obj_to_str(self, person_dict):
        '''Given JSON object returns string'''
        person_string = json.dumps(person_dict, indent = 4, sort_keys=True)
        return person_string