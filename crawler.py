import requests, bs4,  traceback, re
from time import gmtime, strftime, sleep

class crawler():
    def __init__(self):
        self.folder=''
        self.reverse=True
    def getIndexURL(self, page):
        return ''

    def crawl(self,last_page=None,page=1):
        pass
    
    def reverse_page(self):
        last_page=self.total_page-self.page_range+1
        if last_page<1:
            last_page=1
        # first page, last page, order    
        return (self.total_page,last_page-1,-1)
    
    def non_reverse_page(self):
        last_page=self.page_range
        if last_page>self.total_page:
            last_page=self.total_page
        # first page, last page, order    
        return (1,last_page+1,1)
    
    def set_first_last_page(self):
        if self.reverse==True:    
            return self.reverse_page()
        else:
            return self.non_reverse_page()

    
    def CorrectURL(self, url, host):
        if url.startswith('http'):
            return url
        else:
            return host+url
    
    def get_img_url_list(self,reqURL):
        return []
    
 

    

    def getTotalPage(self):
        return self.total_page
    
    
    
    def crawl(self,page=1):
        try:
            self.total_page=self.getTotalPage()
            page_range_tuple=self.set_first_last_page()
            for page in range(*page_range_tuple):
                urls=self.get_page_url_list(page)

                for url in urls:
                    try:
                        url=self.CorrectURL(url, self.urlBase)
                        self.findData(url)
                    except:
                        print(traceback.format_exc())
            
        except:
            print(traceback.format_exc())



class image_crawler(crawler):
    def findData(self,reqURL):
        print('getImage')
        timer=strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        try:
            imgs=self.get_img_url_list(reqURL)
            for url in imgs:
                try:
                    url=self.CorrectURL(url, self.urlBase)
                    self.getData(url,timer)
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        sleep( 5 )


    def getData(self, url,timer):
        picture=requests.get(url)
        fileName=url.split('/')[-1]
        fileName=self.checkFileName(fileName,picture.headers.get('content-type'))
        pictFile=open(self.folder+'/'+timer+'_'+fileName,'wb')
        for temp in picture.iter_content(1024):
            pictFile.write(temp)
        pictFile.close()

    
    def checkFileName(self, fileName,content_type):
        if re.search(r'.*\.jpe?g|.*\.png',fileName)!=None:
            return fileName
        else:
            if content_type=='image/jpeg':
                return fileName+'.jpg'
            elif content_type=='image/png':
                return fileName+'.png'
            elif content_type=='image/svg+xml':
                return fileName+'.svg'
            else:
                return fileName



class text_crawler(crawler):
    def findData(self,reqURL):
        return ''





class housefun_base_crawler(text_crawler):
    def __init__(self):
        self.reverse=False
        self.urlBase='https://buy.housefun.com.tw/'
        self.total_page=1
        self.page_range=67
    def getTotalPage(self):
        return 67
    
    def crawl(self,page=1):
        try:
            self.total_page=self.getTotalPage()
            page_range_tuple=self.set_first_last_page()
            filename='housefun.csv'
            with open(filename, 'w', encoding='utf-8') as out_file:
                out_file.write(f'name,place,area,price,per_area,floor\n')
            for page in range(*page_range_tuple):
                sleep(1)
                print('page ',page, page_range_tuple)
                urls=self.get_page_url_list(page)

            
        except:
            print(traceback.format_exc())


    def get_page_url_list(self,page):
        headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101\
            Safari/537.36', }
        html=requests.get(self.getIndexURL(page), headers=headers)
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        items=beauty.find_all('section', {'class':'m-list-obj'})
        filename='housefun.csv'
        with open(filename, 'a', encoding='utf-8') as out_file:
            for item in items:
                name=item.find('h1').text.replace('\n',' ').replace(',',' ')
                address=item.find("address").text
                ping=item.find("span",{'class':'ping-number'}).find('em').text
                price=item.find("a",{'class':'discount-price'}).find('em').text.replace(',','')
                floor=item.find('span',{'class':'floor'}).text.split('/')[0].split('~')[0].strip()
                try:
                    print(f'{name},{address},{ping},{price},{float(price)/float(ping)},{floor}')
                    out_file.write(f'{name},{address},{ping},{price},{float(price)/float(ping)},{floor}\n')
                except Exception as e:
                    print(f'remove {name}\n',traceback.format_exc())
        # items=beauty.find('ul', class_='waterfall').find_all('li') # //https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page=2
        # urls=[]
        # for item in items:
        #     if (int(item.find('div', class_='auth').find_all('em')[2].find('em').text)>self.watch_threshold 
        #     and item.find('div', class_='auth').find_all('em')[1].find('a').text not in self.blackList):
        #         urls.append(item.find('a')['href'])
        # print('urls',urls)
    
    def getIndexURL(self, page):
        return f'https://buy.housefun.com.tw/region/%E6%96%B0%E5%8C%97%E5%B8%82-%E4%B8%89%E9%87%8D%E5%8D%80_c/?pg={page}'
    


# class model_crawler(jkf_base_crawler):
#     def __init__(self):
#         super().__init__()
#         self.folder='jkf/model'
#         self.blackList=[]
#         self.watch_threshold=1000
#     def getIndexURL(self, page):
#         return f'https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&page={page}'


    

# class beauty_crawler(jkf_base_crawler):
#     def __init__(self):
#         super().__init__()
#         self.folder='jkf/beauty'
#         self.blackList=['假文青派大星']
#         self.watch_threshold=3000
#     def getIndexURL(self, page):
#         return f'https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page={page}'







# indexPage=model_crawler() # 寫真
indexPage=housefun_base_crawler() #輔導級
indexPage.crawl() 