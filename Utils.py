# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup
import Class
def info2list(s):
    pattern = re.compile(r"([a-zA-Z ]*)([0-9]*)(.*)")
    r = re.match(pattern,s)
    if r != None :
        return [r.group(1),r.group(2),r.group(3)]

def get_author_url(author):#得到作者对应的url
    base_url = "https://dblp.uni-trier.de/search/author"
    params = {"q":author.name}
    
    r = requests.get(base_url,params=params)
    
    soup = BeautifulSoup(r.text,"lxml")
    
    res = soup.find_all(class_="result-list")[0]
    
    text = res.previous_sibling.get_text()
    if text != "Exact matches":
        print("No Exact mactches!")
        return 0
    all_li = res.find_all('li')
    get_infos = []#保存从网页得到的作者信息
    sim = []#info 相似度
    url = []
    for x in all_li:
        get_info = info2list(x.get_text())
        JS = Class.JaccardSimilarity(get_info[2],author.info) 
        sim.append(JS.Jaccar())
        get_infos.append(get_info)
        for y in x.find_all('a'):
            url.append(y.get("href"))
    assert len(sim) == len(url)
    if max(sim) == 0:
        print("------------------little info------------------")
        dic = {}
        for i in range(len(url)):
            dic[get_infos[i]] = url[i]
        return dic
    
    else:
        print("------------------compare info------------------")
        n = sim.index(max(sim))
        print("number:",get_infos[n][1])
        print("input_info:",author.info)
        print("get_info:",get_infos[n][2])
        print("similarity:",max(sim))
        return url[n]