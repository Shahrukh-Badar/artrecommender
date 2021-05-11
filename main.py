import pandas as pd
import math
import re


def string_cleaning(data):
    if pd.isna(data):
        return 'dimensionsunavailable'
    else:
        data = data.lower()
        data = 'dimensionsunavailable' if pd.isna(data) else data.replace('\n', ' ').replace('\r', '') \
            .replace('×', 'x').replace(' ', '').replace('approx.', '').strip()
        return data  # data.translate({ord(c): "" for c in "!@$%^&*[]{}:,<>?\|`~-=_+"})


def dimention_transfomation(dim):
    if pd.isna(dim):
        return 'dimensionsunavailable'
    for x in range(0, 10):
        dim = dim.replace(str(x), '#')
    return string_cleaning(dim)


def get_statics_by_occurrence(df, new_col='NewDim'):
    df_grp = df.groupby(new_col).first().reset_index()
    dff = df.groupby([new_col]).count().reset_index()
    dff = dff.rename(columns={'Dimensions': 'count'})
    dff = dff.sort_values(by='count', ascending=False)
    dff = pd.merge(dff, df_grp, on=new_col)
    dff.to_csv('occurrence.csv', encoding='utf8')
    return dff


def data_preprocessing():
    # df = pd.read_csv('MetObjects.csv',nrows=1000)
    columns_to_read = {'Dimensions': 'str'}
    df = pd.read_csv('MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)
    # df = df.loc[df["Dimensions"].str.contains('approx', na=False)]
    df['NewDim'] = df.apply(lambda x: dimention_transfomation(x['Dimensions']), axis=1)
    df['Dimensions'] = df['Dimensions'].fillna('dimensionsunavailable')
    df['Dimensions'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
    df_s = get_statics_by_occurrence(df.copy())
    s = 1


def get_distinct_dimensions(df):
    x = df.Dimensions.unique()
    df = pd.DataFrame(data=x, columns=['Dimensions'])
    df = pd.to_csv('all_dis_dim.csv', encoding='utf8')
    return df


def extract_all_brackets_data(data, brackets=[]):
    bracket = re.search(r"\(([A-Za-z0-9_.]+)\)", data)
    if bracket:
        bracket = bracket.group(0)
        brackets.append(bracket)
        data = data.replace(bracket, '')
        extract_all_brackets_data(data, brackets)

    return brackets


def extract_bracket(data):
    return data[data.index('('):data.index(')') + 1]


def extract_numeric_data(data):
    return data.replace('cm', '').replace(' ', '').replace('(', '').replace(')', '').strip()


def extract_bracket_count(data, original_data=None):
    bracket_open = data.count('(')
    bracket_close = data.count(')')

    return bracket_open if bracket_open == bracket_close else 0


def extract_regex_pattern_2d(data):
    pattern_cm_int = re.search('\d+x{1}\d+', data)
    pattern_cm_decimal = re.search('\d+\.*\d+x{1}\d+\.*\d+', data)
    if pattern_cm_decimal:
        found = pattern_cm_decimal.group(0)
        return found
    elif pattern_cm_int:
        found = pattern_cm_int.group(0)
        return found
    else:
        return 'not_processed'


def extract_regex_pattern_1d(data):
    pattern_cm_int = re.search('\d+', data)
    pattern_cm_decimal = re.search('\d+\.\d+', data)

    if pattern_cm_decimal:
        found = pattern_cm_decimal.group(0)
        return found
    elif pattern_cm_int:
        found = pattern_cm_int.group(0)
        return found
    else:
        return 'not_processed'


def extract_cm_inside_single_bracket(data):
    bracket = extract_bracket(data)
    if 'cm' in bracket and 'x' in bracket:
        bracket = extract_numeric_data(bracket)
        return bracket
        # return bracket  # 'sheet: 1 7/8 x 1 1/8 in. (4.8 x 2.8 cm)'
    elif 'cm' in bracket and 'x' not in bracket:
        bracket = extract_numeric_data(bracket)
        # return bracket  # 'h. 6 1/2 in. (16.5 cm)'
        return bracket


def extract_image_and_sheet_data(data):
    not_in = ['imageandsheet', 'imagesandsheets']
    if any(x in data for x in not_in):
        return data

    return ''.join(
        [x for x in data.split('sheet') if
         'image' in x]) if 'image' in data and 'sheet' in data else data


def extract_dimension_in_cm(dim):
    result = 'not_processed'
    if pd.isna(dim) or dim.lower() == 'dimensionsunavailable':
        return result
    if not 'cm' in dim:
        return result
    dim = 'imagesandsheets(irregular):32x23in.(81.3x58.4cm)'
    cm_str_orig = dim.replace('approx', '').lower()
    cm_str = extract_image_and_sheet_data(cm_str_orig)
    # d2 = extract_regex_pattern_2d(cm_str)
    # d1 = extract_regex_pattern_1d(cm_str)

    # cm_str = 'l.63/4inches17.1cm'
    if extract_bracket_count(cm_str) == 1 and 'cm' not in extract_bracket(cm_str):
        cm_data = cm_str.replace(extract_bracket(cm_str), '')
        cm_data = extract_regex_pattern_2d(cm_str) if 'x' in cm_data else extract_regex_pattern_1d(cm_str)
        # cm_data = extract_regex_pattern_1d(cm_str)
        # return cm_data
        result = cm_data
    elif extract_bracket_count(cm_str) == 0:
        is_regex_found = False
        if 'inches' in cm_str:
            cm_data = [x for x in cm_str.split('inches') if 'cm' in x][0]
            if cm_data:
                found = extract_regex_pattern_2d(cm_data)
                is_regex_found = True if found != 'not_processed' else False
        if not is_regex_found:
            found = extract_regex_pattern_1d(cm_str)
            is_regex_found = True if found != 'not_processed' else False
        result = found if is_regex_found else 'not_processed'
        # return found if is_regex_found else 'not_processed'


    elif 'cm' in cm_str and extract_bracket_count(cm_str) == 1 and \
            ';' not in cm_str and 'cm' not in extract_bracket(cm_str):
        cm_data = [x for x in cm_str.split(extract_bracket(cm_str)) if 'cm' in x][0]
        found = extract_regex_pattern_2d(cm_data)
        result = found
        # return found

    elif extract_bracket_count(cm_str, original_data=cm_str) == 1:
        cm_data = extract_cm_inside_single_bracket(cm_str)
        result = cm_data

    elif extract_bracket_count(cm_str) > 1:
        extracted_brackets = extract_all_brackets_data(cm_str)
        bracket_list = []
        bracket = cm_str
        if ';' in cm_str:
            for x in cm_str.split(';'):
                if extract_bracket_count(x, original_data=cm_str) == 1:
                    bracket = extract_bracket(x)
                    if 'cm' in bracket and 'x' not in bracket:
                        bracket = extract_numeric_data(bracket)
                        bracket_list.append(bracket)
                    bracket = 'x'.join(bracket_list)
        # return bracket  # 'h. 2 1/4 in. (5.7 cm); diam. 7 5/8 in. (19.4 cm)'
        result = bracket
    else:
        general_2d = extract_regex_pattern_2d(cm_str)
        general_1d = extract_regex_pattern_1d(cm_str)
        found = general_2d if general_2d != 'not_processed' else general_1d
        # return 'not_processed' if not found else found
        result = 'not_processed' if not found else found

    if result == 'not_processed':
        s = cm_str
    return result


def pre_process():
    columns_to_read = {'Dimensions': 'str', 'count': 'int', 'NewDim': 'str'}
    df = pd.read_csv('occurrence.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)

    df['dim_clean'] = df.apply(lambda x: extract_dimension_in_cm(x['Dimensions']), axis=1)
    df_np = df[df['dim_clean'] == 'not_processed']
    df_np = df.loc[(df['dim_clean'] == 'not_processed') & (df["NewDim"].str.contains('cm', na=False))]
    df_none = df.loc[(df['dim_clean'].isnull())]  # where cm is outside of bracket
    s = 2


def pre_process_original_data():
    regenerate = False
    if regenerate:
        columns_to_read = {'Object ID': 'int', 'Dimensions': 'str'}
        df = pd.read_csv('MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)
        df['Dimensions'] = df['Dimensions'].fillna('dimensionsunavailable')
        df['Dim_pattern'] = df['Dimensions'].apply(lambda x: dimention_transfomation(x))
        # df['Dim_clean'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
        # df['Dim_processed'] = df.apply(lambda x: extract_dimension_in_cm(x['Dim_clean']), axis=1)
        df = get_statics_by_occurrence(df, 'Dim_pattern')
        # df = df.loc[(~df['Dimensions'].str.contains('cm', na=False))]
        df['Dim_clean'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
        df['Dim_processed'] = df.apply(lambda x: extract_dimension_in_cm(x['Dim_clean']), axis=1)
        df.to_csv('processed.csv', encoding='utf8', index=True)
    else:
        df = pd.read_csv('processed.csv', encoding='utf8')
        df = df.loc[(df["Dim_clean"].str.contains('image', na=False))]
        del df['Dim_processed']
        df['Dim_processed'] = df.apply(lambda x: extract_dimension_in_cm(x['Dim_clean']), axis=1)
        w = 23
    d = 2


# approximately 14.3 x 9.9 cm (5 5/8 x 3 7/8 in.)
# l. 4 3/4 x w. 6 3/4 inches (approx.) 12.1 x 17.1 cm
# mounts approximately: 8.9 x 17.8 cm (3 1/2 x 7 in.)
# approx. each: image: 4 1/4 x 7 1/8 in. (10.8 x 18.1 cm) mount: 10 in. x 11 15/16 in. (25.4 x 30.4 cm)
# s = 'approximately 14.3 x 9.9 cm (5 5/8 x 3 7/8 in.)'
# if 'cm' in s and extract_bracket_count(s) == 1 and \
#         ';' not in s and 'cm' not in extract_bracket(s):
#     cm_data = [x for x in s.split(extract_bracket(s)) if 'cm' in x][0]
#
#     re.search('\d*\.?\d*x{1}\d*\.?\d*', s).group(0)
#
# s = 3
# data_preprocessing()
# pre_process()
pre_process_original_data()
