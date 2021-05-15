import pandas as pd
from text_processor import *
from extractor import Extractor


class DataStatics:
    @staticmethod
    def get_statics():
        columns_to_read = constant.INPUT_FILE_COLUMNS_TO_READ
        df = pd.read_csv(constant.INPUT_FILE_PATH, encoding=constant.INPUT_FILE_ENCODING,
                         usecols=columns_to_read.keys(),
                         dtype=columns_to_read)
        number_of_total_rows = df.shape[0]
        number_of_null_dimensions = df[df[constant.COL_DIMENSIONS].isnull()].shape[0]
        df[constant.COL_DIMENSIONS] = df[constant.COL_DIMENSIONS].fillna(constant.STR_DIMENSION_UNAVAILABLE)
        df['Dimension_pattern'] = df[constant.COL_DIMENSIONS].apply(lambda x: TextProcessor.dimension_transformation(x))

        df_grp = df.groupby('Dimension_pattern').first().reset_index()
        dff = df.groupby(['Dimension_pattern']).count().reset_index()
        dff = dff.rename(columns={constant.COL_DIMENSIONS: 'count'})
        dff = dff.sort_values(by='count', ascending=False)
        dff = pd.merge(dff, df_grp, on='Dimension_pattern')
        number_of_distinct_patterns = dff[dff['Dimension_pattern'] != constant.STR_DIMENSION_UNAVAILABLE].shape[0]

        df = dff
        del dff
        df['Dimension_clean'] = df[constant.COL_DIMENSIONS].apply(lambda x: TextProcessor.string_cleaning(x))
        df['Dimension_processed'] = df.apply(lambda x: Extractor.extract_dimension_in_cm(x['Dimension_clean']), axis=1)
        count_processed_patterns = df.loc[(df['Dimension_processed'] == constant.STR_NOT_PROCESSED)].shape[0]
        count_processed_patterns_no_cm = df.loc[
            (df['Dimension_processed'] == constant.STR_NOT_PROCESSED) & (
                ~df["Dimension_clean"].str.contains(constant.STR_INCHES, na=False))].shape[0]

        print(f'Total number of records: {str(number_of_total_rows)}')
        print(f'Total number of null records: {str(number_of_null_dimensions)}')
        print(f'Total number of unique dimension patterns: {str(number_of_distinct_patterns)}')
        print(
            f'Total number of not processed records: {str(count_processed_patterns)} among which {str(count_processed_patterns_no_cm)} records does not have dimensions in cm.')
