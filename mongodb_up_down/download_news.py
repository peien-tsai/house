from pymongo import MongoClient
import pandas as pd
import time

client = MongoClient("mongodb://root:admin@3.112.130.36")

# db = client.raw_test1
#
# forum_mb = db.mb2009
#
#
# cursor = forum_mb.find().limit(100)
# opinion = pd.DataFrame(list(cursor))
# # print(opinion)
#
# opinion.to_csv('./test_forum1.csv')

# db = client.raw_forum
#
# for year in range(2007, 2021):
#     coll = db['mb' + str(year)]
#     if year < 2009 or year == 2020:
#         cursor = coll.aggregate([{"$sample": {"size": 100}}])
#     else:
#         cursor = coll.aggregate([{"$sample": {"size": 200}}])
#     opinion = pd.DataFrame(list(cursor))
#     opinion.to_csv('./forum_emotion' + str(year) + '.csv', sep='|')
#     time.sleep(1)


db = client.news_cn


# coll = db['cityplan']
# cursor = coll.aggregate([{"$sample": {"size": 100}}])
# opinion = pd.DataFrame(list(cursor))
# opinion.to_csv('E:/cityplan.csv', sep='|')
# time.sleep(1)

file = ['cityplan','rate','public_health','tax','mrt']


for i in file:
    coll = db[i]
    cursor = coll.aggregate([{"$sample": {"size": 50000}}])
    opinion = pd.DataFrame(list(cursor))
    opinion.to_csv('E:/cn_emotion' + '/' + i + '.csv', sep=',')
    time.sleep(1)


# for year in range(2015, 2021):
#     coll = db['mb' + str(year)]
#     if year < 2009 or year == 2020:
#         cursor = coll.aggregate([{"$sample": {"size": 100}}])
#     else:
#         cursor = coll.aggregate([{"$sample": {"size": 200}}])
#     opinion = pd.DataFrame(list(cursor))
#     opinion.to_csv('./forum_emotion' + str(year) + '.csv', sep='|')
#     time.sleep(1)