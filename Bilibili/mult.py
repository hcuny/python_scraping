from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import re
import pandas as pd
import pyprind
import gzip
#from StringIO import StringIO
from io import StringIO
import requests
import json
import multiprocessing
from multiprocessing import Pool
import warnings
warnings.filterwarnings('ignore')
import tqdm


#
def findgenre(s):
    return s.find('div',{'class':'tminfo'}).findAll('span')[0].text

def findrelease(s):
    return s.find('time').text

def findtitle(s):
    return s.find('div',{'class' ,'v-title'}).text

def findup(s):
    return s.find('div',{'class':'upinfo'}).findAll('a')[1].text

def findtag(s):
    return s.find('meta',{ 'name':"keywords"})['content']


def pageDetail(avnum):

    apiweb = "http://api.bilibili.com/archive_stat/stat?aid={}".format(avnum)
    parseApi = urlopen(apiweb).read().decode('utf-8')
    alldata = json.loads(parseApi)['data']
    coinnum = alldata['coin']
    favnum = alldata['favorite']

        
    try:

        if (coinnum>2000 and favnum>4000):       
            
            website='http://www.bilibili.com/video/av{}/'.format(avnum)
            resp=requests.get(website) 
            resp.encoding="utf-8"
            content=resp.text
            soup=BeautifulSoup(content)
            print("Requirement Meet", 'avnum:',avnum,'coin:',coinnum,'fav:',favnum)
            title=findtitle(soup)
            genre=findgenre(soup)
            up=findup(soup)
            tag=findtag(soup)
            release=findrelease(soup)
            print(title,genre)
            hisrank = alldata['his_rank']
            viewnum = alldata['view']     

            with open('Y://results.txt', 'a', encoding='utf-8') as f:
                f.write("title:{}, genre:{}, tag:{}, time:{}, up:{}, view:{}, coin:{}, fav:{}, his_rank:{} \n".\
                        format(title, genre, tag, release, up, viewnum, coinnum, favnum, hisrank))
                
        
                
    except:
        print("Invalid File")

    
def main(urls):
    pool = Pool(4)
    for _ in tqdm.tqdm(pool.imap_unordered(pageDetail, urls), total=len(urls)):
        pass
    #for url in urls:
        #pool.apply_async(pageDetail, (url, ))
    #pool.map(pageDetail, urls)
    pool.close()
    pool.join()

if __name__ == "__main__":
    urls=list(range(100000,1000000))
    main(urls)