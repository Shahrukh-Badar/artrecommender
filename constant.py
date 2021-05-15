CNF_ENABLE_SMART_MATCH = False
CNF_ENABLE_DIRTY_GUESS = True
CNF_ENABLE_DATA_STATICS = False
CNF_DOES_IT_FIT_LOGS = True

INPUT_FILE_PATH = 'openaccess/MetObjects.csv'
INPUT_FILE_ENCODING = 'utf8'
BREAK_POINT = 'q'
COL_OBJECT_ID = 'Object ID'
COL_DIMENSIONS = 'Dimensions'
COL_DIMENSIONS_CLEAN = 'Dimensions_clean'
INPUT_FILE_COLUMNS_TO_READ = {COL_OBJECT_ID: 'int', COL_DIMENSIONS: 'str'}
OUTPUT_FILE_PATH = 'result.pkl'

STR_DIMENSION_UNAVAILABLE = 'dimensionsunavailable'
STR_NOT_PROCESSED = 'not_processed'
STR_ARROW = '->'
STR_INPUT = 'Input'
STR_EXTRACTED = 'Extracted'
STR_INTEGER = 'integer'
STR_CM = 'cm'
STR_INCHES = 'inches'



# MESSAGES
MSG_TRUE = 'True'
MSG_FALSE = 'False'
MSG_OBJECT_ID_INPUT = f'Please enter {COL_OBJECT_ID}.'
MSG_DIMENSION_INPUT = f'Please enter {COL_DIMENSIONS}.'
MSG_APP_CONTINUE = f'Please enter {BREAK_POINT} to quit or enter to continue.'
MSG_OBJECT_ID_NOT_FOUND = f'{COL_OBJECT_ID} not found.'
MSG_OBJECT_ID_INVALID = f'{COL_OBJECT_ID} is invalid.'
MSG_OBJECT_MUST_BE_NUMERIC = f'{COL_OBJECT_ID} must be numeric.'
MSG_RETURNING = f'Returning{STR_ARROW}'
MSG_TRANSFORM_DATA = 'Transforming data.'
MSG_LOAD_DATA = 'Loading data.'
MSG_SAVE_DATA = 'Save processed data.'




###### TEST DATA FOT UNIT TESTS (EXTRACTED FROM MAIN DATASET)
## RAW INPUT , EXPECTED OUTPUT, OBJECT ID
TEST_DATA = [('diam.11/16in.(1.7cm)', '1.7', 3),
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
             ('overall(withoutloop):37x773/4in.(94x197.5cm)overall(withloop):37x801/4in.(94x203.8cm)', '94x197.5',
              70626),
             ('l.17xw.31/2inches43.2x8.9cm', '43.2x8.9', 190801),
             ('h.101/2xw.101/2xd.51/2in.(26.7x26.7x0.14cm)', '26.7x26.7x0.14', 237436)
             ]
