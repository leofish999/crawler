import requests, bs4, os, re, traceback
from time import gmtime, strftime, sleep

class cat_index_page():
    def __init__(self):
        self.folder='ptt/cat'
        self.max_page=4005
        self.minPush=0
    def getIndexURL(self, page):
        return f'/bbs/cat/index{page}.html'
    def checkTitlePattern(self,title):
        return re.search(r'\[.*[認送]養.*\]|\[.*心得.*\]',title)!=None



class beauty_index_page(cat_index_page):
    def __init__(self):
        self.folder='ptt/beauty'
        self.max_page=3736
        self.minPush=10
    def getIndexURL(self, page):
        return f'/bbs/Beauty/index{page}.html'
    def checkTitlePattern(self,title):
        return True


def findPage(index_page,page,last_page):
    print('page',page)
    url_ppt = 'https://www.ptt.cc'
    path = index_page.getIndexURL(page)

    ptthtml = requests.get(url_ppt+path, cookies={'over18':'1'})
    objSoup = bs4.BeautifulSoup(ptthtml.text, 'lxml')

    pttdivs = objSoup.find_all('div', 'r-ent')
    urls=[]
    for pttdiv in pttdivs:
        title=pttdiv.find('div','title').text
        print('push',pttdiv.find('div','nrec').text)
        push=pttdiv.find('div','nrec').text
        if push=='爆':
            push=999
        if not push.isdecimal():
            push=0
        else:
            push=int(push)
        if '本文已被刪除' not in title and index_page.checkTitlePattern(title) and push>=index_page.minPush:
            urls.append(pttdiv.find('div','title').find('a')['href'])
    print('url',urls)
    for url in urls:
        try:
            url=CorrectURL(url, 'https://www.ptt.cc')
            getImage(url, index_page.folder)
        except:
            print(traceback.format_exc())
    
    if last_page< page and page>1:
        findPage(last_page=last_page,page=page-1,index_page=index_page)


def CorrectURL(url, host):
    if url.startswith('http'):
        return url
    else:
        return host+url

def checkFileName(fileName,content_type):
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


def download(url,folder,timer):
    picture=requests.get(url)
    # print('picture status',picture.headers.get('content-length'))
    fileName=url.split('/')[-1]
    fileName=checkFileName(fileName,picture.headers.get('content-type'))
    pictFile=open(folder+'/'+timer+'_'+fileName,'wb')
    for temp in picture.iter_content(1024):
        pictFile.write(temp)
    pictFile.close()




def getImage(reqURL,folder):
    timer=strftime("%Y_%m_%d_%H_%M_%S", gmtime())
    beauty_html = requests.get(reqURL, cookies={'over18':'1'})    # 進入超連結
    beauty_soup = bs4.BeautifulSoup(beauty_html.text, 'lxml')   

    beauty_divs = beauty_soup.find('div', id='main-content')
    photos = []                                                         # 圖片網址
    url_photos = beauty_divs.find_all('a')                              # 找尋所有圖片
    for photo in url_photos:
        href_photo = photo['href']
        if href_photo.startswith('https://i.imgur'):                    # 判斷圖片網址
            photos.append(href_photo)
    
    for url in photos:
            try:
                url=CorrectURL(url, 'https://www.ptt.cc')
                download(url,folder,timer)
            except:
                print(traceback.format_exc())
    sleep( 5 )



index_page=beauty_index_page()
# findPage(index_page=index_page, page=index_page.max_page, last_page=3735)


