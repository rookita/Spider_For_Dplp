# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup
from myclass import *
from concurrent.futures import ThreadPoolExecutor,as_completed
from tqdm import tqdm
from thefuzz import fuzz

    
    
def info2list(s):  #将得到的作者信息分解为list
    pattern = re.compile(r"([a-zA-Z ]*)([0-9]*)(.*)")
    r = re.match(pattern,s)
    if r != None :
        return [r.group(1),r.group(2),r.group(3)]   #group(1)为姓名，group（2）为编号，group（3）为详细信息
    
def get_author_url(author):#得到作者对应的url
    threadpool = ThreadPoolExecutor(10)
    base_url = "https://dblp.uni-trier.de/search/author"
    params = {"q":author.name}
    get_infos = []                                  #保存从网页得到的所有同名作者信息，包括姓名，编号等
    sims = []        
    url = []        
    r = requests.get(base_url,params=params)
    soup = BeautifulSoup(r.text,"lxml")
    result_list = soup.find_all(class_="result-list")[0]
    text = result_list.previous_sibling.get_text()  #返回页面有Exact matches，likely matches等
    if text != "Exact matches":
        print("No Exact mactches!")
        return 0
    all_li = result_list.find_all('li')             
    for i in tqdm(range(len(all_li)),desc = "get_author_url"):
        li = all_li[i]                   
        get_info = info2list(li.get_text())
        sims.append(fuzz.token_sort_ratio(get_info,author.info))
        get_infos.append(get_info)
        for y in li.find_all('a'):
            url.append(y.get("href"))
    assert len(sims) == len(url)
    threadpool.shutdown()
    if max(sims) == 0:
        if (len(url) != 0):
            cmp_info = Cmp_Info(author.name, get_infos[0][1], author.info, get_infos[0][2], 0)
            return url[0]
        else:
            return 0
    else:
        tmp = max(sims)
        n = sims.index(tmp)
        author.url = url[n]
        cmp_info = Cmp_Info(author.name, get_infos[n][1], author.info, get_infos[n][2], tmp)
        return cmp_info,url[n]

        