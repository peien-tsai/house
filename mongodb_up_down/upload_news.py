import os, time, random, re
from pymongo import MongoClient
import pymongo


def input_raw_data(txtpath):
    with open(txtpath, 'r', encoding='utf-8') as txtFile:
        # 讀取 TXT 檔案內容
        content = txtFile.read()
    # 宣告list:把内容的type從str改成list/dict
    return eval(content)  # type為list/dict

'''建立連線'''
#client = MongoClient("mongodb://user:userpassword@ip")

# '''mobile01'''
# db = client.raw_forum  # 切換database
# '''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
# path = r'E:\project\forum\raw_data\new_tpe_2020_0403'  # 设置路径
# dirs = os.listdir(path)  # 获取指定路径下的文件
# '''循环塞資料'''
# for article_name in dirs:  # 讀取每篇文章的名字
#     '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
#     txtpath = os.path.join(path, article_name)
#     content_dict = input_raw_data(txtpath)  # format:{}
#     content_dict["_id"] = int(content_dict["id"])  # 設置_id, 型別為int
#     # print(content_dict['post_date'][:4]) # 年份的字串
#     # coll_name = 'mb' + content_dict['post_date'][:4]
#     coll = db['mb' + content_dict['post_date'][:4]]
#     try:
#         content_id = coll.insert_one(content_dict).inserted_id  # 塞入一筆資料
#         print ("content id is ", content_id)
#     except pymongo.errors.DuplicateKeyError:
#         pass
#     time.sleep(0.5)

# '''ltn'''
# db = client.raw_news
# '''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
# path = r'E:\project\news_crawler\liberty_time_news\estate'  # 设置路径
# dirs = os.listdir(path)  # 获取指定路径下的文件
# '''循环塞資料'''
# for article_name in dirs:  # 讀取每篇文章的名字
#     if 'ym' in article_name:
#         '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
#         txtpath = os.path.join(path, article_name)
#         content_list = input_raw_data(txtpath)  # format:[{}, {}, {}]
#         # content_dict["_id"] = int(content_dict["id"])  # 設置_id, 型別為int
#         # print(content_dict['post_date'][:4]) # 年份的字串
#         # coll_name = 'mb' + content_dict['post_date'][:4]
#         coll = db['ltn' + article_name[2:6]]  # 選擇collection
#         x = coll.insert_many(content_list, ordered=False)  # 批量塞入資料
#         # 输出插入的所有文档对应的 _id 值
#         print(x.inserted_ids)
#         time.sleep(0.5)

# '''hb'''
# db = client.raw_news
# '''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
# path = r'E:\project\news_crawler\raw_data\hbhousenews_peien_20200417'  # 设置路径
# dirs = os.listdir(path)  # 获取指定路径下的文件
# '''循环塞資料'''
# for article_name in dirs:  # 讀取每篇文章的名字
#     '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
#     txtpath = os.path.join(path, article_name)
#     content_list = input_raw_data(txtpath)
#     coll = db['hb']
#     x = coll.insert_many(content_list, ordered=False)
#     # 输出插入的所有文档对应的 _id 值
#     print(x.inserted_ids)
#     time.sleep(0.5)

# '''myhouse'''
# '''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
# path = r'E:\project\news_crawler\raw_data\myhousenews'  # 设置路径
# dirs = os.listdir(path)  # 获取指定路径下的文件
# '''循环塞資料'''
# for article_name in dirs:  # 讀取每篇文章的名字
#     '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
#     txtpath = os.path.join(path, article_name)
#     content_list = input_raw_data(txtpath)
#     coll = db['myhouse']
#     x = coll.insert_many(content_list, ordered=False)
#     # 输出插入的所有文档对应的 _id 值
#     print(x.inserted_ids)
#     time.sleep(0.5)



'''mygonews'''

re_replace = re.compile(",|'|[|]|{|}|")
re_baodao = re.compile("[[][A-Za-z]+[\u4e00-\u9fa5/]+報導[]]")

db = client.raw_news
'''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
path = r'E:\project\news_crawler\raw_data\mygonews\cleared_mygonews'  # 设置路径
dirs = os.listdir(path)  # 获取指定路径下的文件
'''循环塞資料'''
for article_name in dirs:  # 讀取每篇文章的名字
    '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
    txtpath = os.path.join(path, article_name)
    with open(txtpath, 'r', encoding='utf-8') as txtFile:
        # 讀取 TXT 檔案內容
        content_select = re.sub(re_baodao, '"|"', txtFile.read())
        content_split = content_select.split("'內容'")
        content_split_1 = content_split[1].replace("'", '').replace(':[', ":'").replace(']}', "'}").replace('\n', '')
        content_dict = content_split[0] + "'內容'" + content_split_1
        content_dict = eval(content_dict)
    # content_dict["_id"] = int(content_dict["id"])  # 設置_id, 型別為int
    coll = db['mygo' + article_name[:4]]
    try:
        content_id = coll.insert_one(content_dict).inserted_id
        print ("content id is ", content_id)
    except pymongo.errors.DuplicateKeyError:
        pass
    time.sleep(0.5)
