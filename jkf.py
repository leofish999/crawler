import requests, bs4,os, traceback
from time import gmtime, strftime, sleep
test=1
class model_index_page():
    def __init__(self):
        self.folder='jkf/model'
        self.blackList=[]
        self.watch_threshold=1000
    def getIndexURL(self, page):
        return f'https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&page={page}'


class beauty_index_page(model_index_page):
    def __init__(self):
        self.folder='jkf/beauty'
        self.blackList=['假文青派大星']
        self.watch_threshold=3000
    def getIndexURL(self, page):
        return f'https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page={page}'


def download(url,folder,timer):
    picture=requests.get(url)
    fileName=url.split('/')[-1]
    pictFile=open(folder+'/'+timer+'_'+fileName,'wb')
    for temp in picture.iter_content(1024):
        pictFile.write(temp)
    pictFile.close()


def getImage(reqURL,folder):
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
                url=CorrectURL(url, 'https://www.jkforum.net/')
                download(url,folder,timer)
            except:
                print(traceback.format_exc())
    except:
        print(traceback.format_exc())
    sleep( 5 )

def findPage(indexPage,last_page=None,repeatPost=None,page=1):
    print('page',page)
    # html=requests.get(f'https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page={page}') #輔導級
    # html=requests.get(f'https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&page={page}') #寫真
    html=requests.get(indexPage.getIndexURL(page))
    beauty=bs4.BeautifulSoup(html.text,'lxml')
    try:
        # blackList=['假文青派大星']
        total_page=beauty.find('div', class_='pgs').find('div', class_='pg').find('label').find('span').text
        total_page=int(''.join([x for x in total_page if x.isdigit()]))
        items=beauty.find('ul', class_='waterfall').find_all('li') # //https://www.jkforum.net/type-736-853.html?forumdisplay&typeid=853&filter=typeid&typeid=853&forumdisplay=&page=2
        urls=[]
        for item in items:
            if (int(item.find('div', class_='auth').find_all('em')[2].find('em').text)>indexPage.watch_threshold 
            and item.find('div', class_='auth').find_all('em')[1].find('a').text not in indexPage.blackList):
                urls.append(item.find('a')['href'])
        print('urls',urls)
        
        for url in urls:
            try:
                url=CorrectURL(url, 'https://www.jkforum.net/')
                getImage(url, indexPage.folder)
            except:
                print(traceback.format_exc())
    except:
        print(traceback.format_exc())
    sleep( 5 )
    if last_page==None:
        if total_page>page:
            findPage(repeatPost=None,page=page+1)
    elif last_page> page:
        findPage(last_page=last_page,repeatPost=None,page=page+1)


def CorrectURL(url, host):
    if url.startswith('http'):
        return url
    else:
        return host+url

# indexPage=model_index_page() # 寫真
indexPage=beauty_index_page() #輔導級 
findPage(last_page=1,indexPage=indexPage)






