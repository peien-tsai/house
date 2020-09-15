import  requests
from urllib import request
from bs4 import BeautifulSoup
import  os
import re, time, random

hbhouse_news = r"./hbhousenews"
if not os.path.exists(hbhouse_news):
    os.mkdir(hbhouse_news)

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
cookietmp = "_fbp=fb.3.1585832686653.128747363; trkID=7f64019a7d104222a9f3cd12641b68b9; ccsession=202004022104406601a8c03d6c0c67; ccguid=202004022104406601a8c03d6c0c67; _hb_guid=410480e0-ac22-44d5-af63-0055ce4b023a; _ga=GA1.3.1516232468.1585832682; _gid=GA1.3.1479438820.1585832682; _gcl_au=1.1.953030096.1585832682; _atrk_siteuid=nhs6Emi8SExyz47t; _atrk_ssid=C0LQrnUkNo59wWHBHLTzTz; _fbp=fb.3.1585832686653.128747363; adbert_uuid=e6937099-aab8-4423-9ab4-05ba31e092dc; adbert_ia=00f042f201b7f9a0; adbert_fingerprint=ea5eda645e17d5038aeb3a0e09063aae; adbert_st={%22adb5a00493447f6b%22:%22a259b4a9-8c75-462a-b158-4a1825935931%22}; adbert_source=Direct; _cmp=; _cmps=; _cp=; _pd=; adbert_insight=Edge%20customers; appier_utmz=%7B%22csr%22%3A%22www.hbhousing.com.tw%22%2C%22timestamp%22%3A1585832743%2C%22lcsr%22%3A%22www.hbhousing.com.tw%22%7D; _atrk_sessidx=5; appier_pv_counterYBajZ0Eo470lHlH=4; appier_page_isView_YBajZ0Eo470lHlH=bf772b854e7ed9d7b71bba642fe4a68b4af2cf69df5ad7f75c99dd39d4ebd64f"
cookies = {}
for i in cookietmp.split(";"):
    cookies[i.split("=")[0].lstrip()] = i.split("=")[1]
move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\r\u3000"))
page=1
for i in range(1,170):
    output = []
    print("第{}頁".format(i))
    # time.sleep(random.uniform(5, 15))
    url = 'http://www.hbhousing.com.tw/News/List.aspx?Cid=1&Page=%s'%(page)
    res = requests.get(url, headers = headers, cookies = cookies)
    soup = BeautifulSoup(res.text,"lxml")
    date = soup.select('p[class="news__list__label"]')
    article = soup.select("ul[class='news__list-box'] a")
    for j in range(0,len(article)):
        try:
            obj = {}
            title_url = "http://www.hbhousing.com.tw/News/" + article[j]['href']
            res = requests.get(title_url,headers = headers, cookies = cookies)
            title_url_soup = BeautifulSoup(res.text, "lxml")
            head= title_url_soup.select('h3[class="news__header__tit"]')[0].text
            content = title_url_soup.select('p[style="line-height:200%"]')
            [s.extract() for s in title_url_soup.select('li')]
            obj["日期"] = date[j].text.split(' - ')[0]
            obj["標題"] = head
            obj["網址"] = title_url
            obj["內容"] = content[0].text.translate(move).strip()#.replace('\n',"").replace('\n',"")
        except IndexError as e:
            content1 = title_url_soup.select('div[class="newsdetail__main"]')
            [s.extract() for s in title_url_soup.select('li')]
            [d.extract() for d in title_url_soup.select('[class = "newstype01"]')]
            obj["日期"] = date[j].text.split(' - ')[0].strip()
            obj["標題"] = head
            obj["網址"] = title_url
            obj["內容"] = content1[0].text.translate(move).strip()#.replace('\n',"")#.replace('\r',"")           
        output.append(obj)
        print(obj)
        s = str(output)
        with open(hbhouse_news + "/" + "No.{}".format(i) + ".txt", "w", encoding="utf-8") as f:
            f.write(s)
    # time.sleep(random.uniform(5, 15))
    page += 1
