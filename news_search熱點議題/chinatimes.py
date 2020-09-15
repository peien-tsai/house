import requests
from urllib import request
from bs4 import BeautifulSoup
import re, time, random,os,json
import urllib.parse
import os, time, random, re
from pymongo import MongoClient
import pymongo
from pymongo.errors import BulkWriteError

chinatimes_news = r"./chinatimes"
if not os.path.exists(chinatimes_news):
    os.mkdir(chinatimes_news)

# client = MongoClient("mongodb://root:000000@54.249.6.105", retryWrites=False)  #
# db = client.topic_raw_news

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
cookietmp = 'ID=48a24fdf-37b7-d625-5d56-f4064acd0f2e; AviviD_uuid=1101c182-378b-42b0-ad46-c8bdfcaeecd8; DEVICE_ID=BD1BD90D-9091-4D09-947E-B6F32EE2992D; webuserid=1f0a98e5-b640-6f44-65a3-da752ef66f10; __gads=ID=07009fea4dfa8843:T=1586925597:S=ALNI_MYWLRUnGKIVNgV2rXUoqzWnWcc-nQ; IS_TOKENIZED_7259FE3D52BB0CB327CA9CBB066F9C52=true; _ga=GA1.2.1812291329.1586925598; oid=%257B%2522oid%2522%253A%25225c8f8a98-5c24-11e9-adc1-0242ac120004%2522%252C%2522ts%2522%253A1554964685%252C%2522v%2522%253A%25221.0%2522%257D; IS_TOKENIZED_88496FEB6025EA5EF10C835B4D393446=false; Count=3; Sended=Y; _ss_pp_id=2395f69c9296bb600b94a34e1627754c; dable_uid=32352889.1581513708468; OX_plg=pm; _gid=GA1.2.451159728.1587555088; truvid_protected={"val":"c","level":2,"geo":"TW","timestamp":1587555093}; _td=874c8683-8685-4d5d-805d-a2301d98725a; fontType=0; fontSize=3; textColor=0; textAlpha=4; textAlign=-1; bgColor=7; bgAlpha=0; textEdge=4; highlightColor=7; highlightAlpha=0; capitalize=false; scale=false; override=false; LDay=2020/4/23; AMP_TOKEN=%24NOT_FOUND; _gat_UA-123959537-1=1; _gat=1; page_view=9; GED_PLAYLIST_ACTIVITY=W3sidSI6ImVzUTciLCJ0c2wiOjE1ODc2MDYyMjMsIm52IjoxLCJ1cHQiOjE1ODc2MDYyMTQsImx0IjoxNTg3NjA2MjIxfV0.'
cookies = {}
for i in cookietmp.split(";"):
    cookies[i.split("=")[0].lstrip()] = i.split("=")[1]
move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\r\u3000"))
# proxies = {"https": "118.163.83.21:3128", "http": "163.19.235.22:80" }


#找出總共有幾頁
def find_total_page(words):
    url = 'https://www.chinatimes.com/search/' + words + '?chdtv'
    res = requests.get(url, headers=headers,cookies=cookies)
    soup = BeautifulSoup(res.text, "html.parser")
    try:
        lastpage = int(soup.select('li[class="page-item"] a')[-1]['href'].split('=')[1]) + 1
    except IndexError:
        lastpage = 2
    return lastpage
#打開議題資料夾
with open(r'./newsword.txt','r',encoding="utf-8") as f:
    word = f.readlines()
    for k in word:
        lastpage = find_total_page(k.split(' ')[0])
        for j in range (1,lastpage):
            output = []
            print(lastpage)
            print("{}_第{}頁".format(k.replace('\n',''),j))
            url = 'https://www.chinatimes.com/search/' + k.split(' ')[0] + '?page=%s&chdtv' % j
            res = requests.get(url, headers=headers,cookies=cookies)
            soup = BeautifulSoup(res.text, "html.parser")
            article = soup.select('div[class="articlebox-compact"] h3[class="title"] a')
            # print(article)
            # print(len(article))
            # # 抓每篇文章內容
            for i in range(0,len(article)):
                # time.sleep(random.uniform(0,5))
                obj = {}
                title_url = article[i]['href']
                # print(title_url)
                try:
                    if title_url.find("ctweekly") == -1 and title_url.find("wantweekly") == -1 and title_url !='':
                        print("{}_第{}篇".format(title_url,i))
                        res = requests.get(title_url, headers=headers,cookies=cookies)
                        title_url_soup = BeautifulSoup(res.text, "html.parser")
                        date = soup.select('span[class="date"]')
                        obj["日期"] = date[i].text
                        obj["_id"] = title_url.split('/')[-1]
                        head = title_url_soup.select('h1[class="article-title"]')
                        obj["標題"] = head[0].text.translate(move)
                        obj["網址"] = title_url
                        content = title_url_soup.select('div[class="article-body"]')
                        [s.extract() for s in title_url_soup.select('figcaption')]
                        obj["內容"] = content[0].text.translate(move)
                        output.append(obj)
                        # print(obj)
                except IndexError:
                    E = open('IndexError.txt','a',encoding = 'utf-8')
                    E.write('\n')
                    E.write(title_url)
                    E.close()
            save_data_js = json.dumps(output, ensure_ascii=False)
            print(output)

            with open(chinatimes_news + "/" + "{}_{}".format(k.split(' ')[0].replace('\n',''), j) + ".json", "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            # time.sleep(random.uniform(0, 10))


            # # '''chinanews'''
            # # client = MongoClient("mongodb://root:000000@13.231.5.142")
            # # db = client.topic_raw_news
            # coll = db["{}".format(k.split(' ')[1]).replace('\n','')]
            # # try:
            # x = coll.insert_many(output, ordered=False)
            # # except BulkWriteError as bwe:
            # #     print(bwe.details)
            # #     E = open('BulkWriteError.txt', 'a', encoding='utf-8')
            # #     E.write('\n')
            # #     E.write()
            # #     Err =[]
            # #     Err.append(bwe.details)
            # #
            # #     str(Err)
            # #
            #     # you can also take this component and do more analysis
            #     # werrors = bwe.details['writeErrors']
            #     # E.close()
            #     # raise
            # # # 输出插入的所有文档对应的 _id 值
            # print(x.inserted_ids)
            # time.sleep(0.5)
