import pandas as pd
import math


def string_cleaning(data):
    return data if pd.isna(data) else data.replace('\n', ' ').replace('\r', '').replace('×', 'x').lower().strip()


def dimention_transfomation(dim):
    if pd.isna(dim):
        return 'dimensions unavailable'
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
    df['NewDim'] = df.apply(lambda x: dimention_transfomation(x['Dimensions']), axis=1)
    df['Dimensions'] = df['Dimensions'].apply(lambda x: string_cleaning(x))
    df['Dimensions'] = df['Dimensions'].fillna('dimensions unavailable')
    df_s = get_statics_by_occurrence(df.copy())
    s = 1


def get_distinct_dimensions(df):
    x = df.Dimensions.unique()
    df = pd.DataFrame(data=x, columns=['Dimensions'])
    df = pd.to_csv('all_dis_dim.csv', encoding='utf8')
    return df


def extract_dimension_in_cm(dim):
    if pd.isna(dim):
        return dim
    str = dim.lower()
    if str.count('(') == 1 and str.count(')') == 1:
        tmp = str[str.index('('):str.index(')') + 1]
        if 'cm' in tmp and 'x' in tmp:
            tmp = tmp.replace('cm', '').replace(' ', '').replace('(', '').replace(')', '').strip()
            return tmp
        elif 'cm' in tmp  and 'x' not in tmp:
            tmp = tmp.replace('cm', '').replace(' ', '').replace('(', '').replace(')', '').strip()
            return tmp
    elif str.count('(') == 2 and str.count(')') == 2:
        str_dim = []
        tmp = str
        for x in str.split(';'):
            if x.count('(') == 1 and x.count(')') == 1:
                d = x[x.index('('):x.index(')') + 1]
                if 'cm' in d and 'x' not in d:
                    d = d.replace('cm', '').replace(' ', '').replace('(', '').replace(')', '').strip()
                    str_dim.append(d)
                tmp = 'x'.join(str_dim)
        return tmp
    else:
        return dim


def pre_process():
    columns_to_read = {'Dimensions': 'str', 'count': 'int', 'NewDim': 'str'}
    df = pd.read_csv('occurrence.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)
    df['dim_clean'] = df.apply(lambda x: extract_dimension_in_cm(x['Dimensions']), axis=1)
    s = 2


# data_preprocessing()
pre_process()
