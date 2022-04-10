import requests, bs4,  traceback, re
from time import gmtime, strftime, sleep
import pymysql.cursors


class crawler():
    def __init__(self):
        self.folder=''
        self.reverse=True
    def getIndexURL(self, page):
        return ''

    def crawl(self,last_page=None,page=1):
        pass
    
    def reverse_page(self):
        if self.page_range:
            last_page=self.total_page-self.page_range+1
        else:
            last_page=1
        
        if last_page<1:
            last_page=1
        # first page, last page, order    
        return (self.total_page,last_page-1,-1)
    
    def non_reverse_page(self):
        if self.page_range:
            last_page=self.page_range
            if last_page>self.total_page:
                last_page=self.total_page
        else:
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

    def getTotalPage(self):
        return self.total_page
    
    def clearFileOrFolder(self):
        return ''
    
    def findData(self,page):
        return ''
    
    
    def crawl(self,page=1):
        try:
            self.total_page=self.getTotalPage()
            page_range_tuple=self.set_first_last_page()
            self.clearFileOrFolder()
            for page in range(*page_range_tuple):
                print('page ',page, page_range_tuple)
                self.findData(page)
        except:
            print(traceback.format_exc())





class image_crawler(crawler):
    def get_img(self,reqURL):
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
    
    def findData(self,page):
        urls=self.get_page_url_list(page)
        for url in urls:
            try:
                url=self.CorrectURL(url, self.urlBase)
                self.get_img(url)
            except:
                print(traceback.format_exc())


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
    def __init__(self,city,district):
        self.fileName='housefun.csv'
        self.reverse=False
        self.urlBase='https://buy.housefun.com.tw/'
        self.total_page=1
        # page_range=None means page_range=totalPage
        self.page_range=None
        self.use_csv=False
        self.district=district
        self.city=city
        self.headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101\
            Safari/537.36', }
        if not self.use_csv:
            #使用pymysql指令來連接數據庫
            self.connection=pymysql.connect(host='127.0.0.1',port=3307,user='root',password='my-secret-pw',db='house',cursorclass=pymysql.cursors.DictCursor
            )

    def getTotalPage(self):
        html=requests.get(self.getIndexURL(1), headers=self.headers)
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        return int(beauty.find('ul', {'class':'m-pagination-bd'}).find('a',text='最末頁').attrs['data-value'])
    
    def clearFileOrFolder(self):
        if self.use_csv:
            with open(self.fileName, 'w', encoding='utf-8') as out_file:
                out_file.write(f'name,place,area,price,per_area,floor\n')

    def findData(self,page):
        sleep(1)
        urls=self.get_text(page)
    




    def get_text(self,page):
        html=requests.get(self.getIndexURL(page), headers=self.headers)
        beauty=bs4.BeautifulSoup(html.text,'lxml')
        items=beauty.find_all('section', {'class':'m-list-obj'})
        # filename='housefun.csv'
        for item in items:
            name=item.find('h1').text.replace('\n',' ').replace(',',' ')
            address=item.find("address").text
            ping=item.find("span",{'class':'ping-number'}).find('em').text
            price=item.find("a",{'class':'discount-price'}).find('em').text.replace(',','')
            floor=item.find('span',{'class':'floor'}).text.split('/')[0].split('~')[0].strip()
            try:
                print(f'{name},{address},{ping},{price},{float(price)/float(ping)},{floor}')
                if  self.use_csv:
                    with open(self.fileName, 'a', encoding='utf-8') as out_file:
                        out_file.write(f'{name},{address},{ping},{price},{float(price)/float(ping)},{floor}\n')
                else:
                    #從數據庫鏈接中得到cursor的數據結構
                    with self.connection.cursor() as cursor:
                    #在之前建立的user表格基礎上，插入新數據，這裡使用了一個預編譯的小技巧，避免每次都要重複寫sql的語句
                        sql=f"INSERT INTO `housefun_buy`\
                            (`name`, `place`, `area`, `price`, `per_area`, `floor`, district ,create_time) VALUES \
                            ('{name}', '{address}', '{ping}', '{price}', '{float(price)/float(ping)}', '{floor}', '{self.district}', curdate());"
                        # print(sql)
                        cursor.execute(sql)
                        #執行到這一行指令時才是真正改變了數據庫，之前只是緩存在內存中
                        self.connection.commit()
            except Exception as e:
                print(f'remove {name}\n',traceback.format_exc())

    
    def getIndexURL(self, page):
        return f'https://buy.housefun.com.tw/region/{self.city}-{self.district}區_c/?pg={page}'
    


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








indexPage=text_crawler('台北市','北投') #
indexPage.crawl() 