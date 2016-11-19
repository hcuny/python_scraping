#web_scraping with douban Movie 
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import re

#used later in the regular expression
def norm(s): 
    keep = {'a', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'b', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
            'x', 'c', 'v', 'n', 'm', '<', '>', '"', '=', ' ',
            '\n'}
    result = ''
    for c in s:
        if c not in keep:
            result += c
    return result  # result gets rid of things not in 'keep',like a "normalized file


#return total number of movies I have watched
def totmovie(homepage):
    page = urlopen(homepage).read().decode('utf-8')
    bsobj = BeautifulSoup(page, 'html.parser')
    strg = bsobj.findAll('title')[0].get_text()
    numb = re.findall('([0-9]+)', strg)[0]
    num = int(numb)
    return (num)


#get a list of these pages
def get_broadpage(mov_num, homepage):
    page = []
    for k in range(15, mov_num, 15):
        pp = 'https://movie.douban.com/people/53667837/collect?start=%s' % k + '&sort=time&rating=all&filter=all&mode=grid'
        page.append(pp)

    page.insert(0, homepage)
    return page

def parse_page(page):
    district=[] #where the movie produced
    forbid=[] #movies that are forbidened by douban
    avgscore=[] #the average rating of this movie
    
    
    for i in range(len(page)):
        mypage = urlopen(page[i]).read().decode('utf-8')
        mysoup = BeautifulSoup(mypage, 'html.parser')
        pagemovie = mysoup.findAll('div', {"class": "item"})

        for j in range(len(pagemovie)):
            try:
                each = pagemovie[j]('a')[0].get('href', None)
                print(each)
                movie = urlopen(each).read().decode('utf-8')
                thesoup = BeautifulSoup(movie, 'html.parser')
                info1 = str(thesoup.findAll('div', {'id': 'info'}))
                info2 = norm(info1)
                info3 = info2.replace('/', ' ')
                country = re.findall('地区: (.*) 语言', info3)  # will return a list  use Regular Expression
                print(country)
                district.append(country)
                scoretag = thesoup.findAll('strong', {'class': 'll rating_num'})
                avscore = scoretag[0].get_text()
                avgscore.append(avscore)
                print(avscore)

            except:
                forbid.append(each)
                print(i, 'th page', j, 'th movie is forbinden')
                

def main():
    homepage = 'https://movie.douban.com/people/53667837/collect'
    mov_num = totmovie(homepage)
    page=get_broadpage(mov_num,homepage)
    parse_page(page)


if __name__ == '__main__':
    main()

