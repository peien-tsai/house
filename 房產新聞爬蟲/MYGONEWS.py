import requests
import os
from bs4 import BeautifulSoup
import time
import random

resource_path = r'./mygonews'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
for p in range(346, 3875):
    url = 'http://www.mygonews.com/news/searchlistimgtxt?param=param&class=searchnews&page=' + str(p) + '&kw='

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text.replace('<br>', '').replace('<br/>', ''), 'html.parser')
    # print(soup)
    article_url = soup.select('div[class="phot litImgSize"] a')
    # time.sleep(random.uniform(3, 5))
    for i in range(len(article_url)):
        url = article_url[i]['href']
        # print(url)

        title = article_url[i]['href'].split('/')[-1]
        # print(title)

        newstime = soup.select('ul[class="list"] div[class="date"]')[0].text
        # print(time)

        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        text_soup = BeautifulSoup(res.text.replace('<br>', '').replace('<br/>', ''), 'html.parser')
        [s.extract() for s in text_soup('strong')]
        # print(text_soup)
        article_text = text_soup.select('div[class="editbox"]')
        # print(article_text)
        news_json = {'媒體': 'MYGONEWS', '標題': title, '時間': newstime, '網址': url, '內容': article_text}
        # print(news_json)
        with open(r'%s/%s.txt' % (resource_path, newstime + title), 'w', encoding='utf-8') as w:
            w.write(str(news_json))
            w.close()
        print(title + '\n' + '完成儲存')
        print('====================接續下一篇====================')
        # break
        time.sleep(random.uniform(6, 11))
    # break
