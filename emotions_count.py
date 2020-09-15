from opencc import OpenCC
import json,os,re

chinatimes_news_grade = r"./chinatimes_news_grade"
if not os.path.exists(chinatimes_news_grade):
    os.mkdir(chinatimes_news_grade)

#簡體轉繁體
cc = OpenCC('s2twp')
#負面詞
with open(r'C:\Users\Big data\PycharmProjects\PyAI\emodic\NTUSD\ntusd-negative.txt','r',encoding="utf-8") as f:
    content = f.read().replace('\ufeff','')
    negative_vocab = cc.convert(content).split('\n')
print(negative_vocab)
# print(len(negative_vocab))
for j in negative_vocab:
    if len(j) <= 1:
        negative_vocab.remove(j)
# print(len(negative_vocab))

# #正面詞
with open(r'C:\Users\Big data\PycharmProjects\PyAI\emodic\NTUSD\ntusd-positive.txt','r',encoding="utf-8") as f:
    content = f.read().replace('\ufeff','')
    positive_vocab = cc.convert(content).split('\n')
print(positive_vocab)
# print(len(positive_vocab))
for l in positive_vocab:
    if len(l) <= 1:
        positive_vocab.remove(l)
# print(len(positive_vocab))
# #開新聞檔案(chinatimes)
# # article = r'C:\Users\Big data\PycharmProjects\PyETL\chinatimes\cityplan'
# # file_names = os.listdir(article)
# path = r'C:\Users\Big data\PycharmProjects\PyETL\chinatimes'
# dir_names = os.listdir(path)
# for file_names in dir_names:
#     txt_names = os.listdir(path+ '/'+file_names)
#     #每個檔案計算正負面詞數量
#     for file in txt_names:
#         print('file:',file)
#         output = []
#         with open(r'C:\Users\Big data\PycharmProjects\PyETL\chinatimes\{}\{}'.format(file_names,file),'r',encoding="utf-8") as f:
#             content = f.read()
#             js = json.loads(content)
#             for i in js:
#                 pos_word = 0
#                 neg_word = 0
#                 text = i['內容']
#                 for j in negative_vocab:
#                     if j in text and len(j) > 1:
#                         neg_word += text.count(j)
#                 for k in positive_vocab:
#                     if k in text and len(k) > 1:
#                         pos_word += text.count(k)
#                 i['postive'] = pos_word
#                 # print(pos_word)
#                 i['negitive'] = neg_word
#                 i.pop('內容')
#                 output.append(i)
#                 # print(i)
#                 with open(r'C:\Users\Big data\PycharmProjects\PyAI\chinatimes_news_grade\{}\{}'.format(file_names,file.replace(".txt","")) + ".json", "w", encoding="utf-8") as l:
#                     json.dump(output, l, ensure_ascii=False, indent=2)
#                 # print(neg_word)
#         print(output)
#         print(len(output))



# #自由時報
# path = r'C:\Users\Big data\Desktop\ltn_json'
# dir_names = os.listdir(path)
# for file_names in dir_names:
#     txt_names = os.listdir(path+ '/'+file_names)
#     #每個檔案計算正負面詞數量
#     for file in txt_names:
#         print('file:',file)
#         output = []
#         with open(r'C:\Users\Big data\Desktop\ltn_json\{}\{}'.format(file_names,file),'r',encoding="utf-8") as f:
#             content = f.read()
#             js = json.loads(content)
#             for i in js:
#                 pos_word = 0
#                 neg_word = 0
#                 text = i.get('内容')
#                 for j in negative_vocab:
#                     if j in text and len(j) > 1:
#                         neg_word += text.count(j)
#                 for k in positive_vocab:
#                     if k in text and len(k) > 1:
#                         pos_word += text.count(k)
#                 i['postive'] = pos_word
#                 # print(pos_word)
#                 i['negitive'] = neg_word
#                 # del i['內容']
#                 i.pop('内容')
#                 output.append(i)
#                 print(i)
#         with open(r'C:\Users\Big data\Desktop\ltn_json\{}\{}'.format(file_names,file) , "w", encoding="utf-8") as l:
#             json.dump(output, l, ensure_ascii=False, indent=2)
#                 # print(neg_word)
#         print(output)
#         print(len(output))




path = r'C:\Users\Big data\Desktop\upload4'
dir_names = os.listdir(path)
    #每個檔案計算正負面詞數量
for file in dir_names:
    print('file:',file)
    output = []
    with open(r'C:\Users\Big data\Desktop\upload4\{}'.format(file),'r',encoding="utf-8") as f:
        content = f.read()
        js = json.loads(content)
        for i in js:
            pos_word = 0
            neg_word = 0
            text = i.get('内容')
            for j in negative_vocab:
                if j in text and len(j) > 1:
                    neg_word += text.count(j)
            for k in positive_vocab:
                if k in text and len(k) > 1:
                    pos_word += text.count(k)
            i['postive'] = pos_word
            # print(pos_word)
            i['negitive'] = neg_word
            # del i['內容']
            i.pop('内容')
            output.append(i)
            print(i)
    with open(r'C:\Users\Big data\Desktop\upload4\{}'.format(file) , "w", encoding="utf-8") as l:
        json.dump(output, l, ensure_ascii=False, indent=2)
            # print(neg_word)
    print(output)
    print(len(output))



