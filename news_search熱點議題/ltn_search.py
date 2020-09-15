from bs4 import BeautifulSoup
import re, os, time, random, datetime, calendar, json, requests, pymongo
from dateutil.relativedelta import relativedelta
from datetime import date
from pymongo import MongoClient

re_tian = re.compile('保證天天中獎')
re_jour = re.compile('（記者[\u4e00-\u9fa5]*攝）')
re_ling = re.compile('點我訂閱')
re_aut = re.compile('（圖：作者提供）')
re_from = re.compile('（圖擷自[0-9A-Za-z \u4e00-\u9fa5]*）')
re_life = re.compile('life|politics|society|world|local|focus')
re_business = re.compile('business|weeklybiz')
re_jour2 = re.compile('〔[\u4e00-\u9fa5]*／[\u4e00-\u9fa5]*報導〕')

txtpath = r'E:\project\news_crawler\topic_noun\newsword.txt'

'''讀取搜索關鍵字'''
def input_txt(txtpath):
    # 讀取檔案
    re_read = list()
    with open(os.path.join(txtpath), 'r', encoding='utf-8') as txtFile:

        for line in txtFile.readlines():
            line = line.replace('\n','')
            re_read.append(line)
    return re_read  # format:['房改 tax', '炒房 tax', '土地增值稅 tax']

'''獲取内頁網址們'''
def in_crawl(soup):
    news_list = []
    hrefs = soup.select('div[class="whitecon"] ul[class="searchlist boxTitle"] li')
    for href in hrefs:
        in_url = href.select('a')[0]['href']
        print(in_url)
        """建立空字典，存放每筆news的資料"""
        news_json = {}
        news_json['媒體'] = '自由時報-關鍵字：' + keyword
        news_json['網址'] = in_url
        news_json['標題'] = href.select('a')[0].text
        news_json['時間'] = href.select('span')[0].text
        news_json['_id'] = in_url.split('news/')[-1].replace('/', '_')
        '''訪問内頁'''
        in_res = requests.get(url=in_url, headers=headers)
        time.sleep(random.uniform(7, 12))
        in_soup = BeautifulSoup(in_res.text, 'lxml')
        '''内容'''
        in_content = ''
        '''life和politics和society和world和local (網址開頭：https://news.ltn.com.tw/news/'''
        if re.search(re_life, in_url):
            in_content = in_soup.select('div[class="text boxTitle boxText"] p')
            '''business和weeklybiz (網址開頭：https://ec.ltn.com.tw/)'''
        elif re.search(re_business, in_url):
            in_content = in_soup.select('div[class="text"] p')
            '''opinion (網址開頭：https://talk.ltn.com.tw/'''
        elif 'opinion' in in_url:
            in_content = in_soup.select('div[class="cont"] p')
            '''entertainment、supplement、cconsumer (網址開頭：https://ent.ltn.com.tw/'''
        elif 'entertainment' in in_url or 'supplement' in in_url or 'consumer' in in_url:
            in_content = in_soup.select('div[class="news_content"] p')
        in_final = ''
        for i in in_content:
            i = i.text.replace('\n', '')
            if re.search(re_tian, i) == None and re.search(re_ling, i) == None:
                in_final += re.sub(re_jour2, '', re.sub(re_from, '', re.sub(re_aut, '', re.sub(re_jour, '', i))))
        news_json['内容'] = in_final
        print(in_final)
        if in_content != '':
            news_list.append(news_json)
    return news_list

'''寫出資料到json'''
def output_json(filepath, data):
    with open(filepath, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)

dirpath = r'E:\project\news_crawler\raw_data\emotion\ltn_json'

'''自由時報搜索頁'''  # 限制一次只能搜3個月 # 日期格式：2004-11-31
# 表頭
# request method:get
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/80.0.3987.149 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,\
           application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7', 'referer': 'https://news.ltn.com.tw'}
# 關鍵字
for keyword in input_txt(txtpath):
    keyword = keyword.split(' ')[0]
    # 日期設定
    start_time = str('2014-01-01')  # 初始日期2004-01-01
    while date.today() > datetime.datetime.strptime(start_time,'%Y-%m-%d').date():
        end_month_date = datetime.datetime.strptime(start_time,'%Y-%m-%d').date()+ relativedelta(months=2)
        split_date = str(end_month_date).split('-')
        split_date[2]=str(calendar.monthrange(2020,end_month_date.month)[1])
        end_time = '-'.join(split_date)
        print(keyword, '正在爬取：', start_time, end_time)
        '''爬取搜索頁'''
        url = 'https://news.ltn.com.tw/search?keyword={}&conditions=and&start_time={}&end_time={}'.\
            format(keyword, start_time, end_time)
        res = requests.get(url=url, headers=headers)
        time.sleep(random.uniform(7, 12))  # 7, 12
        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup.prettify())
        '''有搜索結果時才往下執行'''
        if soup.select('div[class="whitecon"] a[class="tit"]'):
            # 如果此時間段下的搜索結果>1頁
            if soup.select('div[class="pagination boxTitle"] a[class="p_last"]'):
                last_page = int(soup.select('div[class="pagination boxTitle"] a[class="p_last"]')[0]['href'].split('page=')[-1])+1
                '''設置頁碼'''
                for page in range(1, int(last_page) + 1):
                    '''停止條件'''
                    if page+1 > int(last_page):
                        # with open(os.path.join(dir_path, 'last_month.txt'), 'w', encoding='utf-8') as t:
                        #     t.write(str(news_list))
                        print('大功告成！')
                        break
                    print('正在爬取：第 ' + str(page) + ' 頁')
                    news_list = in_crawl(soup)
                    print(news_list)
                    jsonpath = os.path.join(dirpath, keyword + start_time + '_' + str(page) + '.json')
                    output_json(jsonpath, news_list)
                    '''翻頁'''
                    url = 'https://news.ltn.com.tw/search?keyword={}&conditions=and&start_time={}&end_time={}&page={}'.\
                        format(keyword, start_time, end_time, page + 1)
                    res = requests.get(url=url, headers=headers)
                    time.sleep(random.uniform(4, 8))
                    soup = BeautifulSoup(res.text, 'html.parser')
            else:
                news_list = in_crawl(soup)
                print(news_list)
                jsonpath = os.path.join(dirpath, keyword + start_time + '.json')
                output_json(jsonpath, news_list)
        start_time = str(datetime.datetime.strptime(start_time,'%Y-%m-%d').date()+ relativedelta(months=3))

