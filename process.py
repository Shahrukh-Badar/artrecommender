from text_processor import *
from extractor import Extractor
import constant as constant


class ProcessDimension:
    raw_data = None
    result = None

    def __init__(self):
        self.process()

    @classmethod
    def data_ingestion(cls):
        print(constant.MSG_LOAD_DATA)
        columns_to_read = constant.INPUT_FILE_COLUMNS_TO_READ
        cls.raw_data = pd.read_csv(constant.INPUT_FILE_PATH, encoding=constant.INPUT_FILE_ENCODING,
                                   usecols=columns_to_read.keys(),
                                   dtype=columns_to_read)

    @classmethod
    def data_processing(cls):
        print(constant.MSG_TRANSFORM_DATA)
        df = cls.raw_data
        del cls.raw_data
        df[constant.COL_DIMENSIONS] = df[constant.COL_DIMENSIONS].fillna(constant.STR_DIMENSION_UNAVAILABLE)
        df[constant.COL_DIMENSIONS] = df[constant.COL_DIMENSIONS].apply(lambda x: TextProcessor.string_cleaning(x))
        df[constant.COL_DIMENSIONS_CLEAN] = df[constant.COL_DIMENSIONS]
        df[constant.COL_DIMENSIONS] = df.apply(lambda x: Extractor.extract_dimension_in_cm(x[constant.COL_DIMENSIONS]),
                                               axis=1)

        # df[df[constant.COL_DIMENSIONS] == constant.STR_NOT_PROCESSED]
        del df[constant.COL_DIMENSIONS_CLEAN] # NOTE: put breakpoint here to check the orignal data along with processed data

        df[constant.COL_OBJECT_ID] = pd.to_numeric(df[constant.COL_OBJECT_ID], downcast=constant.STR_INTEGER)
        df.set_index(constant.COL_OBJECT_ID, inplace=True)
        cls.raw_data = df

    @classmethod
    def data_storage(cls):
        print(constant.MSG_SAVE_DATA)
        cls.raw_data.to_pickle(constant.OUTPUT_FILE_PATH)

    @classmethod
    def data_access(cls):
        cls.result = pd.read_pickle(constant.OUTPUT_FILE_PATH)

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
            raise KeyError(constant.MSG_OBJECT_ID_NOT_FOUND)
        except NameError:
            raise NameError(constant.MSG_OBJECT_ID_INVALID)

    @classmethod
    def print_does_it_fit_info(cls, info):
        if constant.CNF_DOES_IT_FIT_LOGS:
            print(info)

    @classmethod
    def does_it_fit(cls, object_id, dimension):
        try:
            ProcessDimension.print_does_it_fit_info(
                f'{constant.STR_INPUT} {constant.COL_OBJECT_ID} {constant.STR_ARROW}' + str(object_id))
            ProcessDimension.print_does_it_fit_info(
                f'{constant.STR_INPUT}  {constant.COL_DIMENSIONS}{constant.STR_ARROW}' + str(dimension))
            data = cls.get_result(int(object_id))[0]
            ProcessDimension.print_does_it_fit_info(
                f'{constant.STR_EXTRACTED} {constant.COL_DIMENSIONS}{constant.STR_ARROW}' + str(data))
            if constant.CNF_ENABLE_SMART_MATCH and all([x in data.split('x') for x in dimension.split('x')]):
                ProcessDimension.print_does_it_fit_info(f'{constant.MSG_RETURNING}{constant.MSG_TRUE}')
                return True
            elif dimension.strip() == data.strip():
                ProcessDimension.print_does_it_fit_info(f'{constant.MSG_RETURNING}{constant.MSG_TRUE}')
                return True
            elif data == constant.STR_NOT_PROCESSED:
                ProcessDimension.print_does_it_fit_info(f'{constant.MSG_RETURNING}{constant.MSG_FALSE}')
                return False
            else:
                ProcessDimension.print_does_it_fit_info(f'{constant.MSG_RETURNING}{constant.MSG_FALSE}')
                return False
        except KeyError:
            ProcessDimension.print_does_it_fit_info(constant.MSG_OBJECT_ID_NOT_FOUND)
            ProcessDimension.print_does_it_fit_info(f'{constant.MSG_RETURNING}{constant.MSG_FALSE}')
            return False
        except ValueError:
            ProcessDimension.print_does_it_fit_info(constant.MSG_OBJECT_MUST_BE_NUMERIC)
            ProcessDimension.print_does_it_fit_info(f'{constant.MSG_RETURNING}{constant.MSG_FALSE}')
            return False
