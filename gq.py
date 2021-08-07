import requests, bs4,os, traceback
from time import gmtime, strftime, sleep
from crawler import non_reverse_crawler


class gq_base_crawler(non_reverse_crawler):
    def __init__(self):
        self.urlBase='https://www.gq.com.tw/'
        self.total_page=999
        self.page_range=2
    # def getTotalPage(self):
        # html=requests.get(self.getIndexURL(1))
        # beauty=bs4.BeautifulSoup(html.text,'lxml')
        # total_page=beauty.find('div', class_='pgs').find('div', class_='pg').find('label').find('span').text
        # total_page=int(''.join([x for x in total_page if x.isdigit()]))
        # return total_page
        
    def get_page_url_list(self,page):
        print(page)
        page_url=self.getIndexURL(page)
        print(page_url)
        html=requests.get(page_url)
        #html=requests.get(f'https://www.gq.com.tw/entertainment/girl?page=2')
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        items=beauty.find_all('div', attrs={'data-test-id':'SliceCategoryLayout'})
        details=[]
        for item in items:
            details=details+item.find_all('p')

        details=[detail for detail in details if detail.text=='girl'] 

        #.find_all('li') # //https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page=2
        urls=[]
        for detail in details:
            urls.append(detail.parent.parent.find('a')['href'])
        print('urls',urls)
        return urls

    
    def get_img_url_list(self,reqURL):
        
        print(reqURL)
        html=requests.get(reqURL)
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        imgs=beauty.find('div', 'NewsletterSliceStickyContainer-p18ox4-2').find_all('img')# //div[@class='pcb'][1]//img
        
        imgs=[img['srcset'].split(' ')[-2] for img in imgs]
        # print(imgs)
        # print(len(imgs))
        
        
        return  imgs

    



# FlexVerticalWrap-ignsy7-4 StickyFlexVerticalWrap-ignsy7-5 FeatureWrap-vogixx-4 kbaQIJ
    

class beauty_crawler(gq_base_crawler):
    def __init__(self):
        super().__init__()
        self.folder='gq/beauty'
    def getIndexURL(self, page):
        return f'https://www.gq.com.tw/entertainment/girl?page={page}'







# indexPage=model_crawler() # 寫真
indexPage=beauty_crawler() #輔導級
indexPage.crawl() 







