'''Class Matcher'''
import pandas as pd

from .extract_and_transform_match import ExtractAndTransformMatch
from .extract_and_transform_source import ExtractAndTransformSource

class Matcher:
    '''Class that calculates:
        - Number of documents matched by doctor's npi
        - Number of documents matched by doctor's name and full address
        - Number of documents matched by practice's full adress
        - Number of documents not matched
    '''

    def __init__(self, full_address, npi, full_name):
        '''Specify what is a full address, npi and full name in the data'''
        self.full_address = full_address
        self.npi = npi
        self.full_name = full_name

    @staticmethod
    def _get_left_unmatched_documents(raw_data_df, source_df, on_key):
        '''Return the documents from the left df that were not matched by the on'''
        merged_df = pd.merge(raw_data_df,
                             source_df,
                             indicator=True,
                             how="outer",
                             on=on_key)
        #choose only the elements that did not match from the raw_data_df
        not_matched_df = merged_df[merged_df['_merge'] == 'left_only']

        selected_columns = []
        column_rename_map = {}

        for column in raw_data_df.columns:
            if column not in not_matched_df.columns:
                selected_columns.append("{}_x".format(column))
                column_rename_map["{}_x".format(column)] = column
            else:
                selected_columns.append(column)

        not_matched_df = not_matched_df[selected_columns]
        return not_matched_df.rename(columns=column_rename_map)

    def _calc_npi_matches_and_df(self, raw_data_df, source_not_unwinded_df):
        '''Calculate matches by npi, and return the documents that were not
        matched'''
        not_matched_by_npi_df = \
            self._get_left_unmatched_documents(raw_data_df,
                                               source_not_unwinded_df,
                                               on_key=self.npi)

        return raw_data_df.shape[0] - not_matched_by_npi_df.shape[0], not_matched_by_npi_df

    def _calc_address_matches_and_df(self, raw_data_df, source_unwinded_df):
        '''Calculate matches by practice's address, and return the documents
        that were not matched'''
        not_matched_by_address_df = \
            self._get_left_unmatched_documents(raw_data_df,
                                               source_unwinded_df,
                                               on_key=self.full_address)

        return raw_data_df.shape[0] - not_matched_by_address_df.shape[0], not_matched_by_address_df

    def _calc_name_and_address_match(self, raw_data_df, source_unwinded_df):
        return pd.merge(raw_data_df,
                        source_unwinded_df,
                        how="inner",
                        on=self.full_name+self.full_address).shape[0]

    @staticmethod
    def _calc_documents_not_matched(left_df, right_df):
        return pd.merge(left_df,
                        right_df,
                        how="inner",
                        on=list(left_df.columns)).shape[0]

    def _calculate_results(self, raw_data_df, source_unwinded_df, source_not_unwinded_df):
        '''Does the inner calculations from the extracted and transformed data'''

        result = {}

        # Get the matches by doctor's npi and the df with the elements of
        # the raw_data_df not matched
        result["Npi Match"], not_matched_by_npi_df = \
            self._calc_npi_matches_and_df(raw_data_df, source_not_unwinded_df)

        # Get the matches by practice's address and the df with the elements of
        # the raw_data_df not matched
        result["Address Match"], not_matched_by_address_df = \
            self._calc_address_matches_and_df(raw_data_df, source_unwinded_df)

        #Get the matches by doctor's name and practice's address
        result["Name And Address Match"] = \
            self._calc_name_and_address_match(raw_data_df, source_unwinded_df)

        #Get the number of documents that weren't matched according to any criteria
        result["Documents Not Matched"] = \
            self._calc_documents_not_matched(
                not_matched_by_npi_df,
                not_matched_by_address_df)

        return result

    def get_solution(self, match_file_path, source_file_path):
        ''' Returns:
        - Number of documents matched by doctor's npi
        - Number of documents matched by doctor's name and full address
        - Number of documents matched by practice's full adress
        - Number of documents not matched

        Inputs:
        - match_file_path: path to match file (csv)
        - source_file_path: path to source file (json)
        '''

        # Extract and transform the source data
        source_data = ExtractAndTransformSource.extract_source_data(source_file_path)
        source_unwinded_df = \
            ExtractAndTransformSource.transform_source_unwinding(source_data,
                                                                 fields_to_unwind=["practices"],
                                                                 fields_not_to_unwind=["doctor"])
        source_not_unwinded_df = \
            ExtractAndTransformSource.transform_source_no_unwinding(
                source_data,
                ["doctor"])

        #Extract and transform the data to match
        raw_data_df = ExtractAndTransformMatch.extract_match_data(match_file_path)
        ExtractAndTransformMatch.transform_match_data(
            raw_data_df,
            fields_to_title_case=["state"],
            fields_to_upper_case=["street", "street_2", "city"])

        return self._calculate_results(raw_data_df, source_unwinded_df, source_not_unwinded_df)
