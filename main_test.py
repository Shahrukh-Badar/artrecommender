import unittest
from extractor import Extractor
import pandas as pd
from process import ProcessDimension
import constant as constants
from unittest.mock import MagicMock
from unittest.mock import patch

class TestProcessDimension(unittest.TestCase):
    ## TEST DATA
    ## RAW INPUT , EXPECTED OUTPUT, Object Id
    test_data = [('diam.11/16in.(1.7cm)', '1.7', 3),
                 ('23/4x31/2x23/4in.(7x8.9x7cm)', '7x8.9x7', 33),
                 (
                     'overall:197/16x13x91/4in.(49.4x33x23.5cm);352oz.18dwt.(10977g)body:h.187/8in.(47.9cm)cover:41/4x413/16in.(10.8x12.2cm);19oz.6dwt.(600.1g)',
                     '49.4x33x23.5', 35),
                 ('h.69/16in.(16.7cm);diam.3in.(7.6cm)', '16.7x7.6', 40),
                 ('overall:h.27/16in.(6.2cm);3oz.19dwt.(123.3g)lip:diam.25/8in.(6.7cm)base:diam.215/16in.(7.4cm)',
                  '6.2x6.7x7.4', 376),
                 ('277/8x343/8x331/4in.(70.8cmx87.3cmx84.5cm)', '70.8x87.3x84.5', 1434),
                 ('diam.24cm(91/2in.)', '24', 42375),
                 (
                     'overall:73/4in.,220grams(19.7cm,7.073troyounces)basediameter:15/8in.(4.1cm)other(heightwithoutstopper):61/8in.(15.6cm)',
                     '19.7x4.1x15.6', 654),
                 ('overall(withoutloop):37x773/4in.(94x197.5cm)overall(withloop):37x801/4in.(94x203.8cm)', '94x197.5',70626),
                 ('l.17xw.31/2inches43.2x8.9cm', '43.2x8.9', 190801),
                 ('h.101/2xw.101/2xd.51/2in.(26.7x26.7x0.14cm)', '26.7x26.7x0.14', 237436)
                 ]

    def test_extract_dimension_in_cm(self):
        for test_case in self.test_data:
            get_dim = Extractor.extract_dimension_in_cm(test_case[0])
            self.assertEqual(get_dim, test_case[1])

    def test_does_it_fit(self):
        df = pd.DataFrame(self.test_data, columns=['raw_dimension', 'extracted_dim', 'Object ID'])
        df = df[['Object ID','extracted_dim','raw_dimension']]
        df['Object ID'] = pd.to_numeric(df['Object ID'], downcast='integer')
        df.set_index('Object ID', inplace=True)
        with patch('process.ProcessDimension.get_result') as mock:

            for test_case in self.test_data:
                mock.return_value = df.loc[test_case[2]]
                get_dim = ProcessDimension.does_it_fit(test_case[2], test_case[1])
                self.assertEqual(get_dim, True)


if __name__ == '__main__':
    unittest.main()
