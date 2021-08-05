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