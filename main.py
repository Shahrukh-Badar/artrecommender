import pandas as pd
import math
import re
from text_processor import *


def string_cleaning(data):
    if pd.isna(data):
        return 'dimensionsunavailable'
    else:
        data = data.lower()
        data = 'dimensionsunavailable' if pd.isna(data) else data.replace('\n', ' ').replace('\r', '') \
            .replace('×', 'x').replace(' ', '').replace('approx.', '').replace('–', '-').replace('()', '').strip()

        return data  # data.translate({ord(c): "" for c in "!@$%^&*[]{}:,<>?\|`~-=_+"})


def dimention_transfomation(dim):
    if pd.isna(dim):
        return 'dimensionsunavailable'
    for x in range(0, 10):
        dim = dim.replace(str(x), '#')
    for x in range(5, 1, -1):
        dim = dim.replace('#' * x, '#')

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


def extract_dimension_in_cm(dim):
    result = 'not_processed'
    if pd.isna(dim) or dim.lower() == 'dimensionsunavailable':
        return result
    if not 'cm' in dim:
        return result
    if ';' in dim:
        s = 2

    cm_str_orig = dim
    cm_str = replace_non_numeric_brackets(dim)
    bracket_data = extract_all_brackets_with_data(cm_str, [])
    bracket_count = len(bracket_data)  # extract_bracket_count(cm_str)

    if bracket_count == 0:
        found = 'not_processed'
        if 'inches' in cm_str:
            cm_data = [x for x in cm_str.split('inches') if 'cm' in x]
            if cm_data:
                found = extract_only_valid_dimension(cm_data[0])
                result = found
    elif bracket_count >= 1:
        if bracket_count in [1, 2, 3] and all(['x' not in x for x in bracket_data]) \
                and all(extract_regex_pattern_1d(x) != 'not_processed' for x in bracket_data):
            cm_data = 'x'.join(extract_regex_pattern_1d(x) for x in bracket_data)
            result = cm_data
        else:
            cm_data = [extract_cm_inside_single_bracket(x) for x in bracket_data if 'cm' in x]
            result = cm_data[0] if cm_data else 'not_processed'  # get only first if multiple pairs exists

    if result == 'not_processed':  # mostly for more than 3 brackets select only first and ambiguios data 'diam:31/4in.(8.3cm)mount:201/2x15x7/8in.(52.1x38.1x2.2cm)'
        result = extract_only_valid_dimension(cm_str)
        if result == 'not_processed':
            s = ""
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
        df['Dim_pattern'] = df['Dimensions'].apply(lambda x: dimention_transfomation(x))
        df = get_statics_by_occurrence(df, 'Dim_pattern')
        # df.to_csv('intermediate.csv', encoding='utf8', index=True)
        # df = pd.read_csv('intermediate.csv', encoding='utf8')
        df['Dim_clean'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
        df['Dim_processed'] = df.apply(lambda x: extract_dimension_in_cm(x['Dim_clean']), axis=1)

        # df.to_csv('processed.csv', encoding='utf8', index=True)
    elif 1 == 12:
        columns_to_read = {'Object ID': 'int', 'Dim_processed': 'str'}
        df = pd.read_csv('processed.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)
        df = pd.Series(data=df['Dim_processed'], index=df['Object ID'])
        s = 2
    else:
        columns_to_read = {'Object ID': 'int', 'Dimensions': 'str'}
        df = pd.read_csv('MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)
        df['Dim_clean'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
        df['Dim_processed'] = df.apply(lambda x: extract_dimension_in_cm(x['Dim_clean']), axis=1)
        df = df.sort_values(by=['Object ID'], ascending=True)
        df.to_csv('processed.csv', encoding='utf8', index=True)
    d = 2


# df['Dimensions'] = df['Dimensions'].fillna('dimensionsunavailable')
# df = df.loc[(df["Dim_clean"].str.contains('image', na=False))]
# del df['Dim_processed']
# df = df.loc[(~df['Dimensions'].str.contains('cm', na=False))]
# df['Dim_clean'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
# df['Dim_processed'] = df.apply(lambda x: extract_dimension_in_cm(x['Dim_clean']), axis=1)
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
# pre_process_original_data()


object_id = 566
data = pd.read_pickle('final.pkl')
s = 2