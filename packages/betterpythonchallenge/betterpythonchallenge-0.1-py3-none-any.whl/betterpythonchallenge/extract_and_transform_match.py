'''Class ExtractAndTransformMatch'''
import pandas as pd

class ExtractAndTransformMatch:
    '''Class that contains static functions for extracting and transforming
    the data from the file to match in csv
    '''
    @staticmethod
    def extract_match_data(file_path):
        '''Use pandas read csv to load the csv into a pandas dataframe'''
        return pd.read_csv(file_path)

    @staticmethod
    def transform_match_data(dataframe, fields_to_title_case, fields_to_upper_case):
        '''Change strings of certain DataFrame columns to title case and upper case'''
        for field in fields_to_upper_case:
            dataframe[field] = \
                dataframe[field].apply(lambda x: x.title() if isinstance(x, str) else x)

        for field in fields_to_title_case:
            dataframe[field] = \
                dataframe[field].apply(lambda x: x.upper() if isinstance(x, str) else x)
