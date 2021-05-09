import pandas as pd
import math
import re


def string_cleaning(data):
    if pd.isna(data):
        if ('approx' in data):
            s = 1
    data = 'dimensionsunavailable' if pd.isna(data) else data.replace('\n', ' ').replace('\r', '') \
        .replace('×', 'x').replace(' ', '').replace('approx', '').lower().strip()
    return data  # data.translate({ord(c): "" for c in "!@$%^&*[]{}:,<>?\|`~-=_+"})


def dimention_transfomation(dim):
    if pd.isna(dim):
        return 'dimensionsunavailable'
    for x in range(0, 10):
        dim = dim.replace(str(x), '#')
    return string_cleaning(dim)


def get_statics_by_occurrence(df):
    df_grp = df.groupby('NewDim').first().reset_index()
    dff = df.groupby(['NewDim']).count().reset_index()
    dff = dff.rename(columns={'Dimensions': 'count'})
    dff = dff.sort_values(by='count', ascending=False)
    dff = pd.merge(dff, df_grp, on='NewDim')
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


def extract_bracket(data):
    return data[data.index('('):data.index(')') + 1]


def extract_numeric_data(data):
    return data.replace('cm', '').replace(' ', '').replace('(', '').replace(')', '').strip()


def extract_bracket_count(data, original_data=None):
    bracket_open = data.count('(')
    bracket_close = data.count(')')

    return bracket_open if bracket_open == bracket_close else 0


def extract_regex_pattern_2d(data):
    pattern_found = re.search('\d*\.?\d*x{1}\d*\.?\d*', data)
    if pattern_found:
        found = pattern_found.group(0)
        return found
    else:
        return 'not_processed'


def extract_regex_pattern_1d(data):
    pattern_found = re.search('\d+\.\d+', data)
    if pattern_found:
        found = pattern_found.group(0)
        return found
    else:
        return 'not_processed'


def extract_dimension_in_cm(dim):
    if pd.isna(dim) or dim.lower() == 'dimensionsunavailable':
        return 'not_processed'
    if not 'cm' in dim:
        return 'not_processed'

    str = dim.replace('approx', '').lower()

    if extract_bracket_count(dim) == 0:
        is_regex_found = False
        if 'inches' in dim:
            cm_data = [x for x in dim.split('inches') if 'cm' in x][0]
            if cm_data:
                found = extract_regex_pattern_2d(cm_data)
                is_regex_found = True if found else False
        if not is_regex_found:
            found = extract_regex_pattern_1d(dim)
            is_regex_found = True if found else False
        return found if is_regex_found else 'not_processed'

    elif 'cm' in str and extract_bracket_count(str) == 1 and \
            ';' not in str and 'cm' not in extract_bracket(str):
        cm_data = [x for x in str.split(extract_bracket(str)) if 'cm' in x][0]
        found = extract_regex_pattern_2d(cm_data)
        return found

    elif extract_bracket_count(str, original_data=str) == 1:
        bracket = extract_bracket(str)
        if 'cm' in bracket and 'x' in bracket:
            bracket = extract_numeric_data(bracket)
            return bracket  # 'sheet: 1 7/8 x 1 1/8 in. (4.8 x 2.8 cm)'
        elif 'cm' in bracket and 'x' not in bracket:
            bracket = extract_numeric_data(bracket)
            return bracket  # 'h. 6 1/2 in. (16.5 cm)'

    elif extract_bracket_count(str) > 1:
        bracket_list = []
        bracket = str
        for x in str.split(';'):
            if extract_bracket_count(x, original_data=str) == 1:
                bracket = extract_bracket(x)
                if 'cm' in bracket and 'x' not in bracket:
                    bracket = extract_numeric_data(bracket)
                    bracket_list.append(bracket)
                bracket = 'x'.join(bracket_list)
        return bracket  # 'h. 2 1/4 in. (5.7 cm); diam. 7 5/8 in. (19.4 cm)'
    else:
        return 'not_processed'


def pre_process():
    columns_to_read = {'Dimensions': 'str', 'count': 'int', 'NewDim': 'str'}
    df = pd.read_csv('occurrence.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)

    df['dim_clean'] = df.apply(lambda x: extract_dimension_in_cm(x['Dimensions']), axis=1)
    df_np = df[df['dim_clean'] == 'not_processed']
    df_np = df.loc[(df['dim_clean'] == 'not_processed') & (df["NewDim"].str.contains('cm', na=False))]
    df_none = df.loc[(df['dim_clean'].isnull())]  # where cm is outside of bracket
    s = 2


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
pre_process()
