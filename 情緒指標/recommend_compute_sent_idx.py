import pandas as pd
import numpy as np
import json

def BI_Simple_func(row):
    pos = row[row == 1].count()  # 把value==1的加起來，得到正向的數量
    neg = row[row == -1].count()
    mid = row[row == 0].count()

    return (pos-neg)/(pos+neg+mid)

def BI_func(row):
    pos = row[row == 1].count()
    neg = row[row == -1].count()

    bi = np.log(1.0 * (1+pos) / (1+neg))

    return bi

jsonpath = r'C:\Users\Big data\Desktop\emo\itn\cityplan.json'

with open(jsonpath, 'r', encoding='utf-8') as jsonfile:
    content_json = json.loads(jsonfile.read())

df = pd.DataFrame(content_json)
# 把日期欄位的值從str轉換成日期
df['時間'] = pd.to_datetime(df['時間'], format="%Y/%m/%d")
# 計算每筆資料的分數
df['score'] = df['postive'] - df['negitive']
# 判斷每筆資料的情緒，正向為1，負向為-1，中性為0
df['polarity'] = df['score'].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
# 按日期把資料分組
grouped = df['polarity'].groupby(df.時間.dt.date)
# 對分好組的每一組數據進行操作，操作方式為自定義的BI_Simple_index
BI_Simple_index = grouped.apply(BI_Simple_func)
# 對分好組的每一組數據進行操作，操作方式為自定義的BI_func
BI_index = grouped.apply(BI_func)
# 橫向合併兩個用自定義function操作的分組資料
sentiment_idx = pd.concat([BI_index.rename('BI'), BI_Simple_index.rename('BI_Simple')], axis=1)
# 補缺失日期
df_date = pd.date_range('2009-09-28','2020-04-23')  # 日期範圍請根據實際數據做調整
sentiment_idx = sentiment_idx.reindex(df_date)
# 對BI_simple計算移動時窗為10的均值
sentiment_idx['BI_Simple_MA'] = sentiment_idx['BI_Simple'].rolling(window=10, center=False).mean()  # 對BI計算移動時窗為15的均值
# 對BI計算移動時窗為10的均值
sentiment_idx['BI_MA'] = sentiment_idx['BI'].rolling(window=10, center=False).mean()  # 對BI計算移動時窗為15的均值


# '''加上房市資料'''
# # 讀取房市資料d.read_csv('./data/sh000001.csv', parse_dates=['date'])
# # # 把日期設為
# quotes = pIndex
# quotes.set_index('date', inplace=True)
# # 把index(日期）變成datetime型別
# sentiment_idx.index = pd.to_datetime(sentiment_idx.index)
# # 用left merge的方式把BI指標和房市資料按列（日期）做合併；使用左/右DataFrame中的row索引做为连接键【其实就是left join】
# merged = pd.merge(sentiment_idx, quotes, how='left', left_index=True, right_index=True)

# 用向後填充的方式處理遺缺值
# merged.fillna(method='ffill', inplace=True)
sentiment_idx.fillna(method='ffill', inplace=True)

# merged.to_csv('merged_sentiment_idx.csv')  # 把資料框寫出到csv檔，內容為每天的情緒BI指標和房市資料
sentiment_idx.to_csv(r'C:\Users\Big data\Desktop\emo\itn\merged_sentiment_idx_itn_city.csv')  # 把資料框寫出到csv檔，內容為每天的情緒BI指標