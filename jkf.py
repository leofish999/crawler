import requests, bs4,os, traceback
from time import gmtime, strftime, sleep
from crawler import crawler


class jkf_base_crawler(crawler):
    def crawl(self,last_page=None,page=1):
        print('page',page)
        html=requests.get(self.getIndexURL(page))
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        try:
            # blackList=['假文青派大星']
            total_page=beauty.find('div', class_='pgs').find('div', class_='pg').find('label').find('span').text
            total_page=int(''.join([x for x in total_page if x.isdigit()]))
            items=beauty.find('ul', class_='waterfall').find_all('li') # //https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page=2
            urls=[]
            for item in items:
                if (int(item.find('div', class_='auth').find_all('em')[2].find('em').text)>self.watch_threshold 
                and item.find('div', class_='auth').find_all('em')[1].find('a').text not in self.blackList):
                    urls.append(item.find('a')['href'])
            print('urls',urls)
            
            for url in urls:
                try:
                    url=self.CorrectURL(url, 'https://www.jkforum.net/')
                    self.getImage(url)
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        sleep( 5 )
        if last_page==None:
            if total_page>page:
                self.crawl(repeatPost=None,page=page+1)
        elif last_page> page:
            self.crawl(last_page=last_page,repeatPost=None,page=page+1)
    
    def getImage(self, reqURL):
        # folder='model'
        timer=strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        print(reqURL)
        html=requests.get(reqURL)
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        try:
            imgs=beauty.find('div', class_='pcb').find_all('img') # //div[@class='pcb'][1]//img
            
            imgs=[img['file'] for img in imgs if img.get('file')!=None]
            print(imgs)
            print(len(imgs))
            
            for url in imgs:
                try:
                    url=self.CorrectURL(url, 'https://www.jkforum.net/')
                    self.download(url,timer)
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        sleep( 5 )

class model_crawler(jkf_base_crawler):
    def __init__(self):
        self.folder='jkf/model'
        self.blackList=[]
        self.watch_threshold=1000
    def getIndexURL(self, page):
        return f'https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&page={page}'


    

class beauty_crawler(jkf_base_crawler):
    def __init__(self):
        self.folder='jkf/beauty'
        self.blackList=['假文青派大星']
        self.watch_threshold=3000
    def getIndexURL(self, page):
        return f'https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page={page}'







indexPage=model_crawler() # 寫真
# indexPage=beauty_crawler() #輔導級
indexPage.crawl(last_page=1) 
# findPage(last_page=1,indexPage=indexPage)






