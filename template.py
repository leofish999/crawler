import requests, bs4,os, traceback
from time import gmtime, strftime, sleep
from crawler import non_reverse_crawler


class gq_base_crawler(non_reverse_crawler):
    def __init__(self):
        self.urlBase='https://www.gq.com.tw/'
        self.total_page=1
        self.page_range=1
        self.total_page=1
    # def getTotalPage(self):
        # html=requests.get(self.getIndexURL(1))
        # beauty=bs4.BeautifulSoup(html.text,'lxml')
        # total_page=beauty.find('div', class_='pgs').find('div', class_='pg').find('label').find('span').text
        # total_page=int(''.join([x for x in total_page if x.isdigit()]))
        # return total_page
        
    def get_page_url_list(self,page):
        html=requests.get(self.getIndexURL(page))
        #html=requests.get(f'https://www.gq.com.tw/entertainment/girl?page=1')
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        items=beauty.find_all('div', attrs={'data-test-id':'SliceCategoryLayout'})
        details=[]
        for item in items:
            details=details+item.find_all('p')


        #.find_all('li') # //https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page=2
        urls=[]
        for detail in details:
                urls.append(detail.parent.parent.find('a')['href'])
        print('urls',urls)
        return urls

    
    def get_img_url_list(self,reqURL):
        
        # print(reqURL)
        # html=requests.get(reqURL)
        # beauty=bs4.BeautifulSoup(html.text,'lxml')
        # imgs=beauty.find('div', class_='pcb').find_all('img') # //div[@class='pcb'][1]//img
        
        # imgs=[img['file'] for img in imgs if img.get('file')!=None]
        # print(imgs)
        # print(len(imgs))
        
        
        return  []

    



# FlexVerticalWrap-ignsy7-4 StickyFlexVerticalWrap-ignsy7-5 FeatureWrap-vogixx-4 kbaQIJ
    

class beauty_crawler(gq_base_crawler):
    def __init__(self):
        super().__init__()
        self.folder='jkf/beauty'
        self.blackList=['假文青派大星']
        self.watch_threshold=3000
    def getIndexURL(self, page):
        return f'https://www.gq.com.tw/entertainment/girl?page={page}'







# indexPage=model_crawler() # 寫真
indexPage=beauty_crawler() #輔導級
indexPage.crawl() 







