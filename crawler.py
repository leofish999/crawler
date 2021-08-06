import requests, bs4,  traceback, re
from time import gmtime, strftime, sleep

class crawler():
    def __init__(self):
        self.folder=''
    def getIndexURL(self, page):
        return ''

    def crawl(self,last_page=None,page=1):
        pass
    
    def download(self, url,timer):
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
    
    def CorrectURL(self, url, host):
        if url.startswith('http'):
            return url
        else:
            return host+url
    
    def get_img_url_list(self,reqURL):
        return []
    
    def getImage(self,reqURL):
        timer=strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        try:
            imgs=self.get_img_url_list(reqURL)
            for url in imgs:
                try:
                    url=self.CorrectURL(url, self.urlBase)
                    self.download(url,timer)
                except:
                    print(traceback.format_exc())
        except:
            print(traceback.format_exc())
        sleep( 5 )
    
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
                        self.getImage(url)
                    except:
                        print(traceback.format_exc())
            
        except:
            print(traceback.format_exc())


class reverse_crawler(crawler):
    def set_first_last_page(self):
        last_page=self.total_page-self.page_range+1
        if last_page<1:
            last_page=1
        # first page, last page, order    
        return (self.total_page,last_page-1,-1)


class non_reverse_crawler(crawler):
    def set_first_last_page(self):
        last_page=self.page_range
        if last_page>self.total_page:
            last_page=self.total_page
        # first page, last page, order    
        return (1,last_page+1,1)
