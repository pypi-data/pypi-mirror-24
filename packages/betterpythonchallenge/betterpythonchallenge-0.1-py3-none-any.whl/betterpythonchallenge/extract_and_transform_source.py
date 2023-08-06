'''Class ExtractAndTransformSource'''
import json

from pandas.io.json import json_normalize

class ExtractAndTransformSource:
    '''Class that contains static functions for extracting and transforming
    the data from the file that contains the source data in json
    '''

    @staticmethod
    def extract_source_data(source_file):
        ''' Form a list of dictionaries from a file with a json doc per line'''
        source_data = []
        with open(source_file) as file:
            for line in file:
                source_data.append(json.loads(line))
        return source_data


    @staticmethod
    def _get_not_unwinded_naming_map(source_series, fields_not_to_unwind):
        '''Form a dict mapping the path to the fields inside fields_not_to_unwind
        to the subfields.
        It is needed in order to use the json_normalize in pandas.io.json.

        Example: {"doctor": {"last_name": "Doe", "first_name": "John"}} will return
        -not_unwinded_naming_map = {"doctor.first_name": "first_name",
                                    "doctor.last_name": "last_name"}'''
        not_unwinded_naming_map = {}
        for field in source_series:
            if field in fields_not_to_unwind:
                for subfield in source_series[field]:
                    not_unwinded_naming_map["{}.{}".format(field, subfield)] = subfield
        return not_unwinded_naming_map

    @staticmethod
    def _get_not_unwinded_fields_path(source_series, fields_not_to_unwind):
        '''Form a list of lists with the path to the fields inside fields_not_to_unwind
        It is needed in order to use the json_normalize in pandas.io.json.

        Example: {"doctor": {"last_name": "Doe", "first_name": "John"}} will return
        -not_unwinded_fields_path = [["doctor", "first_name"],
                                    ["doctor", "last_name"]]
        '''
        not_unwinded_fields_path = []
        not_unwinded_naming_map = {}
        for field in source_series:
            if field in fields_not_to_unwind:
                for subfield in source_series[field]:
                    not_unwinded_fields_path.append([field, subfield])
        return not_unwinded_fields_path

    @staticmethod
    def transform_source_unwinding(source_data, fields_to_unwind, fields_not_to_unwind):
        '''Form a DataFrame from a list of dictionaries.
        Rename columns to follow name conventions as the csv'''
        if len(source_data) != 0:
            not_unwinded_fields_path = \
                ExtractAndTransformSource._get_not_unwinded_fields_path(
                    source_data[0],
                    fields_not_to_unwind)

            not_unwinded_naming_map = \
                ExtractAndTransformSource._get_not_unwinded_naming_map(
                    source_data[0],
                    fields_not_to_unwind)
        else:
            return None
        return json_normalize(source_data,
                              fields_to_unwind,
                              not_unwinded_fields_path).rename(
                                  columns=not_unwinded_naming_map)


    @staticmethod
    def transform_source_no_unwinding(source_data, fields_not_to_unwind):
        '''Form a DataFrame from a list of dictionaries.
        Rename columns to follow name conventions as the csv'''
        if len(source_data) != 0:
            not_unwinded_naming_map = \
                ExtractAndTransformSource._get_not_unwinded_naming_map(
                    source_data[0],
                    fields_not_to_unwind)
        else:
            return None

        return json_normalize(source_data).rename(columns=not_unwinded_naming_map)
