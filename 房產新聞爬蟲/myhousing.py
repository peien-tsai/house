import  requests
from urllib import request
from bs4 import BeautifulSoup
import  os
import re, time, random

myhouse_news = r"./myhousenews"
if not os.path.exists(myhouse_news):
    os.mkdir(myhouse_news)

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
cookietmp = "_fbp=fb.2.1586326393835.1180277142; _ga=GA1.3.206736190.1586326394; _gid=GA1.3.1950968279.1586326394; fc_uid=p; _gat_gtag_UA_31204435_1=1"
cookies = {}
for i in cookietmp.split(";"):
    cookies[i.split("=")[0].lstrip()] = i.split("=")[1]
move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\r\u3000"))
end = '【更多精采內容請上《住展房屋網》官網www.myhousing.com.tw；《住展房屋網》官方粉絲團https://www.facebook.com/myhousingfan。未經授權，請勿轉載】'
for i in range(0,422):
    output = []
    print("第{}頁".format(i))
    # time.sleep(random.uniform(5, 15))
    url = 'https://www.myhousing.com.tw/index.php?option=com_flexicontent&view=category&cid=62&Itemid=558&limitstart=' + str(i*18)
    res = requests.get(url, headers = headers, cookies = cookies)
    soup = BeautifulSoup(res.text,"lxml")
    article = soup.select('span[class="readmore"] a')
    for j in range(0,len(article)):
        obj = {}
        title_url = "https://www.myhousing.com.tw/" + article[j]['href']
        res = requests.get(title_url,headers = headers, cookies = cookies)
        title_url_soup = BeautifulSoup(res.text, "lxml")
        date = soup.select('div[class="value field_created"]')
        obj["日期"] = date[j].text.translate(move)
        head = title_url_soup.select('span[class="fc_item_title"]')[0].text
        obj["標題"] = head.translate(move)
        obj["網址"] = title_url
        content = title_url_soup.select('[class="desc-content field_text"]')
        obj["內容"] = content[0].text.translate(move).replace(end,"")
        output.append(obj)
        print(obj)
        s = str(output)
        with open(myhouse_news + "/" + "No.{}".format(i) + ".txt", "w", encoding="utf-8") as f:
            f.write(s)
    # time.sleep(random.uniform(5, 15))
