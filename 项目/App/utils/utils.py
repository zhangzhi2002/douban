import pandas as pd
from sqlalchemy import create_engine

coon = create_engine('mysql+pymysql://root:123456@localhost:3306/豆瓣')

df = pd.read_sql('select * from movies', coon)


def typeList(type):
    type = df[type].values

    type = map(lambda x: str(x).split(','), type)
    type_list = []
    for i in type:
        for j in i:
            type_list.append(j)
    return type_list


def get_df():
    return df
