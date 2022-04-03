# coding: utf-8
import re
import jieba
import jieba.analyse
import html
import requests
from bs4 import BeautifulSoup,SoupStrainer

class Author:
    def __init__(self,name,school,department,city,country):
        self.name = name
        self.school = school
        self.department = department
        self.city = city
        self.country = country
        self.info = school + ", " + department + ", " + city + ", " + country
    def update_name(self,name):
        self.name = name
    def update_school(self,school):
        self.school = school
    def update_department(self,department):
        self.department = department
    def update_city(self,city):
        self.city = city
    def update_country(self,country):
        self.country = country

class Paper:
    def __init__(self,year,title,Bibtex):
        self.year = year
        self.title = title
        self.Bibtex = Bibtex

class Papers:
    def __init__(self,base_url,author_name):
        self.base_url = base_url
        self.paper = []
        self.years = []
        self.author_name = author_name
        
    def parse(self):
        print("-----------------start parsing!------------------")
        r = requests.get(self.base_url)
        
        only_hideable_tags = SoupStrainer("div",class_="hideable")
        
        soup = BeautifulSoup(r.text,"lxml",parse_only = only_hideable_tags)
        res = soup.find_all(class_="hideable")
        res = res[0:len(res)-1]
        for r in res:
            ul = r.find_all('ul',class_="publ-list")[0]#ul子节点
            assert ul.contents[0]['class'][0] == 'year'
            for li in ul.contents:
                if li['class'][0] == 'year':
                    year = li.get_text()
                    self.years.append(year)
                    
                else:
                    drop_down = li.find_all('nav',class_ = 'publ')[0].find_all('li',class_='drop-down')[1]
                    body = drop_down.contents[1]
                    link_li = body.contents[1].contents
                    #print(link_li[0])
                    title = li.find_all('span',class_="title")[0].get_text()
                    
                    Bibtex = link_li[0].find_all('a')[0].get('href')
                    tmp = self.parse_bibtex(Bibtex)
                    Bibtex = tmp
                    
                    paper = Paper(year,title,Bibtex)
                    
                    self.paper.append(paper)
        print("-----------------end parsing!------------------")
    
    def parse_bibtex(self,Bibtex):#得到对应的bibtex url
        r = requests.get(Bibtex)
        only_p_tags = SoupStrainer("p")
        soup = BeautifulSoup(r.text,"lxml",parse_only = only_p_tags)
        a = soup.find_all('p',string = "download as .bib file")[0].contents[0]
        return a.get('href')
    
    def print_paper(self):
        print("-----------------paper info!------------------")
        for x in self.paper:
            print("year:",x.year)
            print("title:",x.title)
            print("Bibtex:",x.Bibtex)

class JaccardSimilarity(object):
    """
    jaccard相似度
    """
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    def Jaccar(self):
        # 去除停用词
        #jieba.analyse.set_stop_words('./files/stopwords.txt')

        # 分词与关键词提取
        keywords_x = self.extract_keyword(self.s1)
        keywords_y = self.extract_keyword(self.s2)

        # jaccard相似度计算
        intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
        union = len(list(set(keywords_x).union(set(keywords_y))))
        # 除零处理
        sim = float(intersection)/union if union != 0 else 0
        return sim

