import random
import logging as log
from .operations import CSVToDataFrame

FILE_PATH = "data/"
DEMO_FILE_NAME = "demo.csv"

class TruthOrDare:
    def __init__(self):
        self.get_data()

    def get_data(self, file_name = DEMO_FILE_NAME):
        file = CSVToDataFrame(FILE_PATH + file_name)
        self.all_df = file.read_csv()
        self.truth_df = self.all_df[self.all_df['type'] == 'Truth']
        self.dare_df = self.all_df[self.all_df['type'] == 'Dare']
        log.info(self.truth_df)
        log.info(self.dare_df)

    def get_random(self, df):
        try:
            random_index = random.randint(0, len(df) - 1)
            question = df.iloc[random_index]['summary']
        except Exception as error:
            log.error(error)
        return question

    def get_truth(self):
        try:
            question = self.get_random(self.truth_df)
        except Exception as error:
            log.error(error)
        log.info(question)
        return question
    
    def get_dare(self):
        try:
            action = self.get_random(self.dare_df)
        except Exception as error:
            log.error(error)
        log.info(action)
        return action
