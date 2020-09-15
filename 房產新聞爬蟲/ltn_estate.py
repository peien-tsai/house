import requests
from bs4 import BeautifulSoup
import re, os, time, random
import json

dir_path = os.path.join(os.curdir, 'estate')
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

'''地產主頁'''
url = 'https://estate.ltn.com.tw/news'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/80.0.3987.149 Safari/537.36'}
res = requests.get(url=url, headers=headers)
time.sleep(random.uniform(7, 18))
soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())

'''獲取最後一頁的頁碼'''  # 只爬取N-1頁，所以要+1
'''
=====================要做測試的話可以直接從此處更改===========================
'''
last_page = int(soup.select('div[class="page boxTitle boxText"] a[data-desc="最後一頁"]')[0]['href'].split('/')[-1]) + 1
# last_page = 11 # 爬取N-1頁
'''
============================================================================
'''

"""建立空list，用於存放所有新聞的dict"""
news_list = []
"""建立空list，用於記錄年月"""
ym_list = ['none']
try:
    '''設置頁碼'''
    for page in range(1, int(last_page) + 1):
        '''停止條件'''
        if page+1 > int(last_page):
            with open(os.path.join(dir_path, 'last_month.txt'), 'w', encoding='utf-8') as t:
                t.write(str(news_list))
            print('大功告成！')
            break
        print('正在爬取：第 ' + str(page) + ' 頁')
        '''獲取内頁網址們'''
        hrefs = soup.select('div[class="box news boxTitle"] a')
        for href in hrefs:
            if hrefs.index(href) % 3 == 1:
                in_url = 'https://estate.ltn.com.tw/' + href['href']
                print(in_url)
                """建立空字典，存放每筆news的資料"""
                news_json = {}
                news_json['媒體'] = '自由時報-地產'
                news_json['網址'] = in_url
                news_json['標題'] = href.text
                # print(href.text)
                '''訪問内頁'''
                in_res = requests.get(url=in_url, headers=headers)
                time.sleep(random.uniform(45, 75))
                in_soup = BeautifulSoup(in_res.text, 'html.parser')
                # print(in_soup.prettify())

                date = in_soup.select('div[class="container page-name boxTitle"] span[class="time"]')[0].text
                news_json['時間'] = date
                '''取得新聞年份&月份->用於分開儲存'''
                year_month = date.split('/')[0] + date.split('/')[1]
                if year_month != ym_list[-1]:
                    """寫出上個月的新聞"""
                    with open(os.path.join(dir_path, 'ym' + ym_list[-1] + '.txt'), 'w', encoding='utf-8') as t:
                        t.write(str(news_list))
                        # json.dump(str)
                    ym_list.append(year_month)
                    news_list = []
                '''取得内文'''
                cra_inpage = in_soup.select('div[class="wordright"] p')
                join_list = []
                for i in range(len(cra_inpage) - 1):
                    join_list.append(cra_inpage[i].text.strip())
                news_json['内容'] = ','.join(join_list)[:-1]
                news_list.append(news_json)
                '''寫出最舊月資料'''
        '''翻頁'''
        url = 'https://estate.ltn.com.tw/news/{}'.format(page+1)
        res = requests.get(url=url, headers=headers)
        time.sleep(random.uniform(50, 100))
        soup = BeautifulSoup(res.text, 'html.parser')
except:
    print('出問題：' + str(in_url))