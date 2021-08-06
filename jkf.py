import requests, bs4,os, traceback
from time import gmtime, strftime, sleep
from crawler import crawler


class jkf_base_crawler(crawler):
    def __init__(self,last_page=None):
        self.urlBase='https://www.jkforum.net/'
        self.last_page=last_page
        self.total_page=1
        self.page_range=1
    def getTotalPage(self):
        html=requests.get(self.getIndexURL(1))
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        total_page=beauty.find('div', class_='pgs').find('div', class_='pg').find('label').find('span').text
        total_page=int(''.join([x for x in total_page if x.isdigit()]))
        return total_page
    def set_first_last_page(self):
        last_page=self.page_range
        if last_page>self.total_page:
            last_page=self.total_page
        # first page, last page, order    
        return (1,last_page+1,1)
    def get_page_url_list(self,page):
        html=requests.get(self.getIndexURL(page))
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        items=beauty.find('ul', class_='waterfall').find_all('li') # //https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page=2
        urls=[]
        for item in items:
            if (int(item.find('div', class_='auth').find_all('em')[2].find('em').text)>self.watch_threshold 
            and item.find('div', class_='auth').find_all('em')[1].find('a').text not in self.blackList):
                urls.append(item.find('a')['href'])
        print('urls',urls)
        return urls

    


    
    def get_img_url_list(self,reqURL):
        
        print(reqURL)
        html=requests.get(reqURL)
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        imgs=beauty.find('div', class_='pcb').find_all('img') # //div[@class='pcb'][1]//img
        
        imgs=[img['file'] for img in imgs if img.get('file')!=None]
        print(imgs)
        print(len(imgs))
        
        
        return  imgs

    


class model_crawler(jkf_base_crawler):
    def __init__(self):
        super().__init__()
        self.folder='jkf/model'
        self.blackList=[]
        self.watch_threshold=1000
    def getIndexURL(self, page):
        return f'https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&page={page}'


    

class beauty_crawler(jkf_base_crawler):
    def __init__(self):
        super().__init__()
        self.folder='jkf/beauty'
        self.blackList=['假文青派大星']
        self.watch_threshold=3000
    def getIndexURL(self, page):
        return f'https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page={page}'







# indexPage=model_crawler(last_page=1) # 寫真
indexPage=beauty_crawler() #輔導級
indexPage.crawl() 
# findPage(last_page=1,indexPage=indexPage)






