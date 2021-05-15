from text_processor import *
from extractor import Extractor


class ProcessDimension:
    raw_data = None
    result = None

    def __init__(self):
        self.process()

    @classmethod
    def data_ingestion(cls):
        columns_to_read = {'Object ID': 'int', 'Dimensions': 'str'}
        cls.raw_data = pd.read_csv('openaccess/MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(),
                                   dtype=columns_to_read)

    @classmethod
    def data_processing(cls):
        df = cls.raw_data
        del cls.raw_data
        df['Dimensions'] = df['Dimensions'].fillna('dimensionsunavailable')
        df['Dimensions'] = df['Dimensions'].apply(lambda x: TextProcessor.string_cleaning(x))
        df['Dimensions'] = df.apply(lambda x: Extractor.extract_dimension_in_cm(x['Dimensions']), axis=1)
        df['Object ID'] = pd.to_numeric(df['Object ID'], downcast='integer')
        df.set_index('Object ID', inplace=True)
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
    def get_result(cls, object_id):
        try:
            return cls.result.loc[object_id]
        except KeyError:
            raise KeyError('Object Id not fount.')
        except NameError:
            raise NameError('Object Id is invalid.')

    @classmethod
    def does_it_fit(cls, object_id, dimension):
        smart_match = False
        try:
            print('Input object id->' + str(object_id))
            print('Input dimension->' + str(dimension))
            data = cls.get_result(int(object_id))[0]
            print('Extracted dimension->' + str(data))
            if smart_match and all([x in data.split('x') for x in dimension.split('x')]):
                print('Returning->True')
                return True
            elif dimension.strip() == data.strip():
                print('Returning->True')
                return True
            elif data == 'not_processed':
                print('Returning->False')
                return False
            else:
                print('Returning->False')
                return False
        except KeyError:
            print('Object Id not found.')
            print('Returning->False')
            return False
        except ValueError:
            print('Object Id must be numeric.')
            print('Returning->False')
            return False
