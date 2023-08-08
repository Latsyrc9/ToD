import pandas as pd
import os

class Files:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_csv_files_from_folder(self):
        csv_files = []
        for file in os.listdir(self.folder_path):
            if file.endswith(".csv"):
                csv_files.append(file)
        return csv_files

class CSVToDataFrame:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_csv(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found.")
            return None
        