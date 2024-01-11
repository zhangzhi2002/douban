import pandas as pd

df = pd.read_csv('tempDate.csv', encoding='utf-8')
df.fillna("暂无", inplace=True)
df.drop_duplicates(subset=["电影名字"], inplace=True)  # 删除重复行，基于"电影名字"列
print(df)
