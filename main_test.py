import unittest
from extractor import Extractor
import pandas as pd
from process import ProcessDimension
import constant as constants
from unittest.mock import patch


class TestProcessDimension(unittest.TestCase):
    test_data = constants.TEST_DATA

    def test_extract_dimension_in_cm(self):
        for test_case in self.test_data:
            get_dim = Extractor.extract_dimension_in_cm(test_case[0])
            self.assertEqual(get_dim, test_case[1])

    def test_does_it_fit(self):
        df = pd.DataFrame(self.test_data, columns=['raw_dimension', 'extracted_dim', constants.COL_OBJECT_ID])
        df = df[[constants.COL_OBJECT_ID, 'extracted_dim', 'raw_dimension']]
        df['Object ID'] = pd.to_numeric(df[constants.COL_OBJECT_ID], downcast=constants.STR_INTEGER)
        df.set_index(constants.COL_OBJECT_ID, inplace=True)
        with patch('process.ProcessDimension.get_result') as mock:
            for test_case in self.test_data:
                mock.return_value = df.loc[test_case[2]]
                get_dim = ProcessDimension.does_it_fit(test_case[2], test_case[1])
                self.assertEqual(get_dim, True)


if __name__ == '__main__':
    unittest.main()
