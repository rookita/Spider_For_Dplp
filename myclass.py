# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup,SoupStrainer
from concurrent.futures import ThreadPoolExecutor,as_completed
from tqdm import tqdm

class Cmp_Info():
    def __init__(self,name,number,info_from_input,info_from_dplp,sim):
        self.name = name
        self.number = number
        self.info_from_input = info_from_input
        self.info_from_dplp = info_from_dplp
        self.sim = sim
    def print_cmp_info(self):
        print("name:",self.name)
        print("number:",self.number)
        print("info_from_input:",self.info_from_input)
        print("info_from_dplp:",self.info_from_dplp)
        print("sim:",self.sim)
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

class Papers:       #所有论文
    def __init__(self,author):
        self.base_url = author.url        #即显示所有论文的url
        self.papers = []
        self.years = []
        self.author_name = author.name
        self.threadpool = ThreadPoolExecutor(max_workers = 30)
        
    def parse(self):
        r = requests.get(self.base_url)
        only_hideable_tags = SoupStrainer("div",class_="hideable")
        soup = BeautifulSoup(r.text,"lxml",parse_only = only_hideable_tags) #只解析class为hideable的div
        hideables = soup.find_all(class_= "hideable")
        hideables = hideables[0:len(hideables)-1]
        tasks = []               
        for hideable in hideables:                                   
            publ_list = hideable.find_all('ul',class_="publ-list")[0] 
            for i in range(len(publ_list.contents)):
                class_ = publ_list.contents[i]['class'][0]
                if  class_== 'year':
                    year = publ_list.contents[i].get_text()
                elif re.match(r'entry.*', class_):  
                    #self.parse_paper(publ_list.contents[i],year)
                    try:
                        tasks.append(self.threadpool.submit(self.parse_paper,publ_list.contents[i], year))
                    except:
                        print("thread error")
                else:
                    print(publ_list.contents[i]['class'])
            for future in as_completed(tasks):
                pass
    def parse_paper(self,li,year):
        drop_down = li.find_all('nav',class_ = 'publ')[0].find_all('li',class_='drop-down')[1]
        body = drop_down.contents[1]
        Bibtex_link = body.contents[1].contents
        Bibtex = Bibtex_link[0].find_all('a')[0].get('href')
        try:
            tmp = self.threadpool.submit(self.parse_bibtex(Bibtex))
            #tmp = self.parse_bibtex(Bibtex)
        except:
            tmp = "error"
        Bibtex = tmp
        #Bibtex = "None"
        title = li.find_all('span',class_="title")[0].get_text()
        paper = Paper(year,title,Bibtex)
        self.papers.append(paper)
                 
    def parse_bibtex(self,Bibtex):  #得到对应的bibtex url
        r = requests.get(Bibtex)
        only_a_tags = SoupStrainer("a")
        soup = BeautifulSoup(r.text,"lxml",parse_only = only_a_tags)
        a = soup.find_all('a',string = "download as .bib file")[0]
        return a.get('href')
    
    def print_paper(self):
        for x in self.papers:
            print("year:",x.year)
            print("title:",x.title)
            print("Bibtex:",x.Bibtex)
        print("The number of papers:",len(self.papers))

