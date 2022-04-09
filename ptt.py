import requests, bs4, re, traceback
from time import gmtime, strftime, sleep
from crawler import image_crawler
class ptt_base_crawler(image_crawler):
    def __init__(self,page_range):
        self.page_range=page_range
        self.urlBase='https://www.ptt.cc'
        self.reverse=True
    def checkTitlePattern(self,title):
        return True
    def get_page_url_list(self,page):
        ptthtml = requests.get(self.getIndexURL(page), cookies={'over18':'1'})
        objSoup = bs4.BeautifulSoup(ptthtml.text, 'lxml')
        pttdivs = objSoup.find_all('div', 'r-ent')
        urls=[]
        for pttdiv in pttdivs:
            title=pttdiv.find('div','title').text
            print('push',pttdiv.find('div','nrec').text)
            push=pttdiv.find('div','nrec').text
            if push=='爆':
                push=999
            elif not push.isdecimal():
                push=0
            else:
                push=int(push)
            if '本文已被刪除' not in title and self.checkTitlePattern(title) and push>=self.minPush:
                urls.append(pttdiv.find('div','title').find('a')['href'])
        print('url',urls)
        return urls

    def get_img_url_list(self,reqURL):
        
        beauty_html = requests.get(reqURL, cookies={'over18':'1'})    # 進入超連結
        beauty_soup = bs4.BeautifulSoup(beauty_html.text, 'lxml')   

        beauty_divs = beauty_soup.find('div', id='main-content')
        photos = []                                                         # 圖片網址
        url_photos = beauty_divs.find_all('a')                              # 找尋所有圖片
        for photo in url_photos:
            href_photo = photo['href']
            if href_photo.startswith('https://i.imgur'):                    # 判斷圖片網址
                photos.append(href_photo)
        
        return photos 

            



class cat_crawler(ptt_base_crawler):
    def __init__(self,page_range=1):
        super().__init__(page_range)
        self.folder='ptt/cat'
        self.total_page=4005
        self.minPush=0
    def getIndexURL(self, page):
        return f'https://www.ptt.cc/bbs/cat/index{page}.html'
    def checkTitlePattern(self,title):
        return re.search(r'\[.*[認送]養.*\]|\[.*心得.*\]',title)!=None
    


class beauty_crawler(ptt_base_crawler):
    def __init__(self,page_range=1):
        super().__init__(page_range)
        self.folder='ptt/beauty'
        self.total_page=3736
        self.minPush=10
    def getIndexURL(self, page):
        return f'https://www.ptt.cc/bbs/Beauty/index{page}.html'
    def checkTitlePattern(self,title):
        return '帥哥' not in title




index_page=beauty_crawler()
# index_page=cat_crawler()

index_page.crawl()


