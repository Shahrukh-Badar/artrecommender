import pandas as pd
import math


def dimention_transfomation(dim):
    if pd.isna(dim):
        return dim
    for x in range(0, 10):
        dim = dim.replace(str(x), '#')
    return dim.replace('\r', '').replace('\n', '').strip()


def get_statics_by_occurrence(df):
    df_grp = df.groupby('NewDim').first().reset_index()
    dff = df.groupby(['NewDim']).count().reset_index()
    dff = dff.rename(columns={'Dimensions': 'count'})
    dff = dff.sort_values(by='count', ascending=False)
    dff = pd.merge(dff, df_grp, on='NewDim')
    dff.to_csv('occurrence.csv', encoding='utf8')
    return dff


def get_distinct_dimensions(df):
    x = df.Dimensions.unique()
    df = pd.DataFrame(data=x, columns=['Dimensions'])
    df = pd.to_csv('all_dis_dim.csv', encoding='utf8')
    return df


def data_preprocessing():
    # df = pd.read_csv('MetObjects.csv',nrows=1000)
    columns_to_read = {'Dimensions': 'str'}
    df = pd.read_csv('MetObjects.csv', encoding='utf8', usecols=columns_to_read.keys(), dtype=columns_to_read)
    df['NewDim'] = df.apply(lambda x: dimention_transfomation(x['Dimensions']), axis=1)

    df_s = get_statics_by_occurrence(df.copy())
    s = 1


data_preprocessing()
