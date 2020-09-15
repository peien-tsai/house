from ckiptagger import construct_dictionary, WS, POS, NER
import re, os, time, random, datetime, calendar, math
from dateutil.relativedelta import relativedelta
from datetime import date

re_replace = re.compile(",|'|[|]|{|}|")
re_baodao = re.compile("[[][A-Za-z]+[\u4e00-\u9fa5/]+報導[]]")

ws = WS(r'E:\\data')
pos = POS(r'E:\\data')
ner = NER(r'E:\\data')

dir_path = os.path.join(os.curdir, 'topic_noun', 'key_nouns')
if not os.path.exists(dir_path):
    os.mkdir(dir_path)

# 斷詞function（含自定義詞典）
def split_word(sentence):  # 輸入格式為list的raw content
    with open(r'E:\project\nlp\dictionary\dic_del_one_merge_sy.txt', 'r', encoding="utf-8") as f:
        userdict = f.readlines()
        user_dict = {}
        # print(userdict)
        for i in userdict:
            user_dict[i.replace('\n', '')] = 1
        f.close()
    dictionary = construct_dictionary(user_dict)

    word_s = ws(sentence,
                sentence_segmentation=True,
                segment_delimiter_set={'?', '？', '!', '！', '。', ',', '，', ';', ':', '、', '，', '|'},
                recommend_dictionary=dictionary)  # 建議詞典
                # coerce_dictionary=dictionary)  # 强制詞典
    return word_s  # format:[['A','B','C'], ['A','B','C'], ['D']]

# 單篇篩選出名詞
def combine_wandp(w_list, p_list, cp_list):
    assert len(w_list) == len(p_list)
    for w, p in zip(w_list, p_list):
        if 'Na' == p or 'Nb' == p or 'Nc' == p:
            cp_list.append(w)

# 把每篇篩選完的名詞放進list，再把每篇的list放進大list（保留文章分隔）
def find_noun(total_article_content, word_s, word_p):
    b = list()
    for i, sentence in enumerate(total_article_content):  # 進入每篇文章
        each_art = list()
        combine_wandp(word_s[i], word_p[i], each_art)
        b.append(each_art)
    return b

# output txt
def output_txt(txtpath, key_nouns):
    if not os.path.exists(txtpath):
        f = open(txtpath, 'w', encoding = 'utf-8')
        f.close()
    # 將名詞寫出至txt檔
    with open(os.path.join(txtpath), 'a', encoding='utf-8') as txtFile:
        for article in key_nouns:
            txtFile.write(str(article) + '\n')

# input txt
def input_txt(txtpath):
    # 讀取檔案
    re_read = list()
    with open(os.path.join(txtpath), 'r', encoding='utf-8') as txtFile:
        for line in txtFile.readlines():
            line = eval(line.replace('\n',''))
            re_read.append(line)
    return re_read

# input raw data(txt)
def input_raw_data(txtpath):
    with open(txtpath, 'r', encoding='utf-8') as txtFile:
        # 讀取 TXT 檔案內容
        content = txtFile.read()
    # 宣告list:把内容的type從str改成list/dict
    return eval(content)  # type為list/dict

# idf
def idf(corpus):
    idfs = {}
    d = 0.0
    # 統計詞出現次數
    for doc in corpus:
        d += 1
        counted = []
        for word in doc:
            if not word in counted:
                counted.append(word)
                if word in idfs:
                    idfs[word] += 1
                else:
                    idfs[word] = 1
    # 計算每個詞idf
    for word in idfs:
        idfs[word] = math.log(d/float(idfs[word]))
    return idfs

# tf-idf
def tf_idf(re_read):
    corpus = re_read # 此處獲取的語料庫是每篇文章的分詞結果列表的列表
    idfs = idf(corpus)
    all_words = []
    for doc in corpus:
        tfidfs = {}
        for word in doc:
            if word in tfidfs:
                tfidfs[word] += 1
            else:
                tfidfs[word] = 1
        for word in tfidfs:
            tfidfs[word] *= idfs[word]
        all_words.append(tfidfs)
    return all_words

# 把分數在1.8分以下的丟掉
def select_nouns(all_words):
    d_list = []
    for tfidfs in all_words:
        for k, v in tfidfs.items():
            if v >= 1.8:
                d_list.append(k)
    return d_list

# 不丟掉名詞
def raw_nouns(all_words):
    e_list = []
    for tfidfs in all_words:
        for k, v in tfidfs.items():
            e_list.append(k)
    return e_list

# 自由時報
def noun_ltn():
    year_month = {'year':['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
                  '2020month':['01','02','03'], '2015month':['05', '06', '07', '08', '09', '10', '11', '12'],
                  'month':[]}
    for year in range(2015, int(date.today().year)+1 ):
        if year == 2015:
            year_month['month'] = year_month['2015month']
        elif year == 2020:
            year_month['month'] = year_month['2020month']
        else:
            year_month['month'] = year_month['year']
        for month in year_month['month']:
            raw_content = []
            num = int(month)
            with open(os.path.join(os.curdir, 'liberty_time_news', 'estate', 'ym' + str(year) + month + '.txt'), 'r', encoding='utf-8')\
                    as txtFile:
                # 讀取 TXT 檔案內容
                content = txtFile.read()
            # 宣告list:把内容的type從str改成list
            content_list = eval(content)  # type為list
            for dic in content_list:
                each_news = dic['標題'] + '|' + dic['内容']
                raw_content.append(each_news)  # 把每篇文章内容加進list: raw_content
            '''分批分詞，每10篇為一批'''
            # 批次數量
            if len(raw_content) % 10 == 0:
                split_times = len(raw_content) // 10
            else:
                split_times = len(raw_content) // 10 + 1
            for each_pitch in range(split_times):
                print('正在處理：{}年{}月-第{}批'.format(year, month, each_pitch))
                '''每批文章範圍'''
                content_range = raw_content[each_pitch*10:(1+each_pitch)*10]
                '''每批斷詞，使用已定義好的斷詞function'''
                word_s = split_word(content_range)  # 斷詞后的結果，有區隔文章
                '''每批詞性標注，使用ckip自帶function'''
                word_p = pos(word_s)  # 詞性標注后的結果，有區隔文章
                '''找出名詞（保留文章區隔）'''
                key_nouns = find_noun(content_range, word_s, word_p)  # format: [[],[],[]]
                del word_s, word_p  # 釋放記憶體
                '''# 將名詞寫出至txt檔'''
                txtpath = os.path.join(os.curdir, 'topic_noun', 'key_nouns', 'key_select', 'ltn_hb_myhouse', 'key' + str(year) + '.txt')
                output_txt(txtpath, key_nouns)
                del key_nouns  # 釋放記憶體

# 住商不動產+住展
def noun_hb_myhouse(news_name):  # news_name=hbhousenews_peien_20200417或myhousenews
    '''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
    path = os.path.join(os.curdir, 'raw_data', news_name)  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    '''循环判断：使用os.path.splitext()方法筛选出指定类型的文件'''
    for article_name in dirs:  # 讀取每篇文章的名字
        # if '2020' in article_name:
        raw_content = []
        '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
        txtpath = os.path.join(os.curdir, 'raw_data', news_name, article_name)
        content_list = input_raw_data(txtpath)
        print('正在處理：', news_name, article_name)
        for dic in content_list:
            each_news = dic['標題'] + '|' + dic['內容']
            raw_content.append(each_news)  # 把每篇文章内容加進list: raw_content
        '''使用已定義好的斷詞function'''
        word_s = split_word(raw_content)
        '''每批詞性標注，使用ckip自帶function'''
        word_p = pos(word_s)  # 詞性標注后的結果，有區隔文章
        '''找出名詞（保留文章區隔）'''
        key_nouns = find_noun(raw_content, word_s, word_p)  # format: [[],[],[]]
        del word_s, word_p  # 釋放記憶體
        '''# 將名詞寫出至txt檔'''
        txtpath = os.path.join(os.curdir, 'topic_noun', 'key_nouns', 'key_select', 'ltn_hb_myhouse',
                               'key' + article_name[:4] + '.txt')
        output_txt(txtpath, key_nouns)
        del key_nouns  # 釋放記憶體

# mygonews
def noun_mygo():
    '''準備工作：设置指定的路径，使用os.listdir() 方法获取路径下所有的文件'''
    path = r'E:\project\news_crawler\mygonews\cleared_mygonews'  # 设置路径
    dirs = os.listdir(path)  # 获取指定路径下的文件
    '''循环判断：使用os.path.splitext()方法筛选出指定类型的文件'''
    for year in range(2010,2021):
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            print('正在處理：', 'mygones', year, '年', month, '月')
            raw_content = []
            for article_name in dirs:  # 讀取每篇文章的名字
                if str(year) in article_name[:4] and month in article_name[5:7]:
                    '''讀取 TXT 檔案內容, 宣告list:把内容的type從str改成list'''
                    txtpath = os.path.join(os.curdir, 'mygonews', 'cleared_mygonews', article_name)
                    # content_dict = input_raw_data(txtpath)
                    with open(txtpath, 'r', encoding='utf-8') as txtFile:
                        # 讀取 TXT 檔案內容
                        content_select = re.sub(re_baodao, '"|"', txtFile.read())
                        content_split = content_select.split("'內容'")
                        content_split_1 = content_split[1].replace("'", '').replace(':[', ":'").replace(']}', "'}").replace('\n', '')
                        content_dict = content_split[0] + "'內容'" + content_split_1
                        content_dict = eval(content_dict)
                        # print(content_dict)
                        # print(type(content_dict))
                    each_news = content_dict['標題'] + '|' + content_dict['內容']
                    raw_content.append(each_news)  # 把每篇文章内容加進list: raw_content
            '''分批分詞，每10篇為一批'''
            # 批次數量
            if len(raw_content) % 10 == 0:
                split_times = len(raw_content) // 10
            else:
                split_times = len(raw_content) // 10 + 1
            for each_pitch in range(split_times):
                '''每批文章範圍'''
                content_range = raw_content[each_pitch * 10:(1 + each_pitch) * 10]
                '''每批斷詞，使用已定義好的斷詞function'''
                # word_s = str(split_word(content_range)).replace(",", "").replace("'", "").replace("[", "").\
                #     replace("]", "").strip()  # 斷詞后的結果，有區隔文章
                word_s = split_word(content_range)
                '''每批詞性標注，使用ckip自帶function'''
                word_p = pos(word_s)  # 詞性標注后的結果，有區隔文章
                '''找出名詞（保留文章區隔）'''
                key_nouns = find_noun(content_range, word_s, word_p)  # format: [[],[],[]]
                del word_s, word_p  # 釋放記憶體
                '''# 將名詞寫出至txt檔'''
                txtpath = os.path.join(os.curdir, 'topic_noun', 'key_nouns', 'key_q' + str(year) + '.txt')
                output_txt(txtpath, key_nouns)
                del key_nouns  # 釋放記憶體

# 產出結果
def final_word():
    """篩選重要名詞"""
    # for year in range(2010, int(date.today().year)+1 ):
    for year in range(2006, 2010):
        '''讀取整年名詞'''
        txtpath = os.path.join(os.curdir, 'topic_noun', 'key_nouns', 'key_select', 'merge', 'key' + str(year) + '.txt')
        re_read = input_txt(txtpath)
        '''tf-idf'''
        all_words = tf_idf(re_read)
        '''把分數在1.8以下的名詞丟掉'''
        final_word_list = select_nouns(all_words)
        '''統計詞頻&排序'''
        tf_n = {}
        for word in final_word_list:
            if word in tf_n:
                tf_n[word] += 1
            else:
                tf_n[word] = 1
        topic_result = sorted(tf_n.items(), key=lambda d: d[1], reverse=True)
        '''輸出結果'''
        topicpath = os.path.join(os.curdir, 'topic_noun', 'key_nouns', 'topic', 'topic' + str(year) + '.txt')
        output_txt(txtpath=topicpath, key_nouns=topic_result)
        del topic_result, final_word_list

        '''不要丟掉名詞'''
        raw_word_list = raw_nouns(all_words)
        '''統計詞頻&排序'''
        tf_n = {}
        for word in raw_word_list:
            if word in tf_n:
                tf_n[word] += 1
            else:
                tf_n[word] = 1
        topic_result = sorted(tf_n.items(), key=lambda d: d[1], reverse=True)
        '''輸出結果'''
        topicpath = os.path.join(os.curdir, 'topic_noun', 'key_nouns', 'topic', 'topic_raw' + str(year) + '.txt')
        output_txt(txtpath=topicpath, key_nouns=topic_result)
        del topic_result, re_read, raw_word_list, all_words

def main():
    """斷詞&根據詞性篩選名詞"""
    # noun_ltn()
    # noun_hb_myhouse(news_name='hbhousenews_peien_20200417')
    # noun_hb_myhouse(news_name='myhousenews')
    # noun_mygo()
    """篩選名詞"""
    final_word()

if __name__ == '__main__':

    main()
    print('大功告成！')
