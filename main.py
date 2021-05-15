from text_processor import *
from Extractor import Extractor

def get_statics():
    columns_to_read = {'Dimensions': 'str'}
    df = pd.read_csv('openaccess/MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(),
                     dtype=columns_to_read)
    number_of_total_rows = df.shape[0]
    number_of_null_dimensions = df[df['Dimensions'].isnull()].shape[0]
    df['Dimensions'] = df['Dimensions'].fillna('dimensionsunavailable')
    df['Dimension_pattern'] = df['Dimensions'].apply(lambda x: TextProcessor.dimension_transformation(x))

    df_grp = df.groupby('Dimension_pattern').first().reset_index()
    dff = df.groupby(['Dimension_pattern']).count().reset_index()
    dff = dff.rename(columns={'Dimensions': 'count'})
    dff = dff.sort_values(by='count', ascending=False)
    dff = pd.merge(dff, df_grp, on='Dimension_pattern')
    number_of_distinct_patterns = dff[dff['Dimension_pattern'] != 'dimensionsunavailable'].shape[0]

    df = dff
    del dff
    df['Dimension_clean'] = df['Dimensions'].apply(lambda x: TextProcessor.string_cleaning(x))
    df['Dimension_processed'] = df.apply(lambda x: Extractor.extract_dimension_in_cm(x['Dimension_clean']), axis=1)
    count_processed_patterns = df.loc[(df['Dimension_processed'] == 'not_processed')].shape[0]
    count_processed_patterns_no_cm = df.loc[
        (df['Dimension_processed'] == 'not_processed') & (~df["Dimension_clean"].str.contains('cm', na=False))].shape[0]

    s = 1


def get_statics_by_occurrence(df, new_col='NewDim'):
    df_grp = df.groupby(new_col).first().reset_index()
    dff = df.groupby([new_col]).count().reset_index()
    dff = dff.rename(columns={'Dimensions': 'count'})
    dff = dff.sort_values(by='count', ascending=False)
    dff = pd.merge(dff, df_grp, on=new_col)
    dff.to_csv('occurrence.csv', encoding='utf8')
    return dff



class ProcessDimension:
    raw_data = None
    result = None

    def __init__(self):
        self.process()

    @classmethod
    def data_ingestion(cls):
        columns_to_read = {'Object ID': 'int', 'Dimensions': 'str'}
        cls.raw_data = pd.read_csv('openaccess/MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(),
                                   dtype=columns_to_read, nrows=10000)

    @classmethod
    def data_processing(cls):
        df = cls.raw_data
        del cls.raw_data
        df['Dimensions'] = df['Dimensions'].fillna('dimensionsunavailable')
        df['Dimensions'] = df['Dimensions'].apply(lambda x: TextProcessor.string_cleaning(x))
        df['Dimensions'] = df.apply(lambda x: Extractor.extract_dimension_in_cm(x['Dimensions']), axis=1)
        df = df.sort_values(by=['Object ID'], ascending=True)
        df = pd.Series(data=df['Dimensions'], index=df['Object ID'])
        cls.raw_data = df

    @classmethod
    def data_storage(cls):
        cls.raw_data.to_pickle('result.pkl')

    @classmethod
    def data_access(cls):
        cls.result = pd.read_pickle('result.pkl')

    @classmethod
    def process(cls):
        cls.data_ingestion()
        cls.data_processing()
        cls.data_storage()
        cls.data_access()

    @classmethod
    def does_it_fit(cls, object_id, dimensions):
        smart_match = False
        try:
            print('input->' + str(object_id) + ',' + str(dimensions))
            data = cls.result[int(object_id)]
            print(data)
            if smart_match and all([x in data.split('x') for x in dimensions.split('x')]):
                return True
            elif dimensions.strip() == data.strip():
                return True
            elif data == 'not_processed':
                return False
            else:
                return False
        except KeyError:
            print('Object Id not found.')
            return False
        except ValueError:
            print('Object Id must be numeric.')
            return False


# if __name__ == "__main__":
#     process_dimension = ProcessDimension()
#     while True:
#         print('Please enter object id.')
#         object_id = input()  # 1000
#         print('Please enter dimension.')
#         dimension = input()  # '135.6x186.4x46.7'
#         if dimension:
#             print(process_dimension.does_it_fit(object_id, dimension))
#             print('Please enter q to quit and enter to continue.')
#             stop = input()
#             if stop.strip() == 'q':
#                 break


get_statics()
