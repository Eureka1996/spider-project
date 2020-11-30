# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import urllib.parse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os
import shutil

loadExecutor = ThreadPoolExecutor(max_workers=50)
localPath = 'D:\\MyDrivers\\update\\photo5'
personNames=["沈梦瑶","王雨纯","陆萱萱","就是阿朱啊","陶喜乐",
             "方子萱","杨晨晨"," 林文文","周于希","仓井优香",
             "玥儿玥","果儿","艾栗栗","七七","杨紫嫣","薛琪琪",
             "夏美酱","艾小青","赵小米","柳侑绮","苏雨彤","糯美子",
             "小热巴","王语纯","陈思琪","夏诗诗","张雨萌","林子欣","美七","鱼子酱",
             "徐安安","安然","顾奈奈","尹菲","肉肉","梦心月","梦心玥","唐安琪",
             "言沫","软软","软而","噜噜妞儿","陈小喵","白茹雪","芝芝","九月生",
             "优优","朱可儿","姬玉露","还是陈梵妮"]


def getPictureLink(url):
    name = parseUrl(url, '//div[@class="c_title"]/h1[1]/text()')[1]
    links = parseUrl(url, '//div[@class="c_img"]/a[1]/img[1]/@src')[1]
    return (name[0].replace("/",""),links[0])

def parseUrl(url,tag):
    result = []
    html = None
    while html is None:
        try:
            html = urllib.request.urlopen(url,timeout=60).read()
            html = etree.HTML(html)
            result = html.xpath(tag)
        except Exception as e:
            pass
            # print('parseUrl error:%s,%s'%(str(type(e)),url))
    return (html,result)

def loadPicture(url,localPath,filename,pictureIndex,reLoadTime):
    if reLoadTime > 5:
        return

    personName = ""
    for n in personNames:
        index = filename.find(n)
        if index != -1:
            personName = n
            break

    if personName == "":
        return
    filenameTmp = '%s\\%s' % (localPath, filename)
    newFileNameTmp = '%s\\%s\\%s' % (localPath,personName,filename)
    personNamePath = '%s\\%s' % (localPath,personName)
    if not os.path.exists(personNamePath):
        os.makedirs(personNamePath)

    try:
        if os.path.exists(filenameTmp):
            print('\t\t转移图片(%s,%s)' % (filenameTmp,newFileNameTmp))
            shutil.move(filenameTmp,newFileNameTmp)
        elif os.path.exists(newFileNameTmp):
            print('\t\t(%d,%d,%d)图片已经存在：%s' % (pictureIndex[0], pictureIndex[1], pictureIndex[2], filename))
        else:
            print('\t\t(%d,%d,%d)下载图片%d：%s,%s' % (
            pictureIndex[0], pictureIndex[1], pictureIndex[2], reLoadTime, filename, url))
            pictureContent = urllib.request.urlopen(url, timeout=120).read()
            with open(newFileNameTmp, "wb") as f:
                f.write(pictureContent)
            print('\t\t(%d,%d,%d)下载图片完成：%s' % (pictureIndex[0], pictureIndex[1], pictureIndex[2], filename))

    except Exception as e:
        loadPicture(url, localPath, filename, pictureIndex, reLoadTime+1)


def getFilename(pictureUrl,pictureName):
    numIndex = str(pictureUrl).rfind('/')
    extendTmp = pictureUrl[numIndex+1:]
    filename = '%s%s' % (pictureName,extendTmp)
    return filename

# 获取图片集的信息：名称，图片数量
def getPictureSetDesc(url):
    divCount = 2
    parseUrlResult = parseUrl(url,'//div[@class="main"]/div[' + str(divCount) + ']/a/@title')
    # 获取图片名称
    pictureSetNames = parseUrlResult[1]
    while len(pictureSetNames) == 0:
        divCount += 1
        pictureSetNames = parseUrlResult[0].xpath('//div[@class="main"]/div[' + str(divCount) + ']/a/@title')
    pictureSetName = pictureSetNames[0]

    # 获取图片页数
    pageDivCount = divCount + 1
    pageColumn = parseUrlResult[0].xpath('//div[@class="main"]/div[' + str(pageDivCount) + ']/a[last()-1]')
    while len(pageColumn) == 0:
        pageDivCount += 1
        pageColumn = parseUrlResult[0].xpath('//div[@class="main"]/div[' + str(pageDivCount) + ']/a[last()-1]')
    pictureCount = pageColumn[0].text
    return (pictureSetName,pictureCount)

def load(urlName):
    urls = crawPictureSetUrls(urlName, 'http://www.quantuwang.cc/')
    for url in urls:
        link = getPictureLink(url)
        loadPicture(link[1], localPath, link[0] + '.jpg', (0, 0, 1), 0)



def crawPictureSetUrls(url,urlPrix):
    suffies = parseUrl(url, '//div[@class="c_page"]/a/@href')[1]
    res = [url]
    for suffix in suffies:
        res.append(urlPrix+suffix)

    return res

def getAllUrlsByName(url,urlPrix):
    allUrlsTemp = parseUrl(url,'//div[@class="index_left"]/div[@class="c_page"]/a/@href')[1];
    allUrls = []
    allUrls.append(url)
    for ut in allUrlsTemp:
        allUrls.append(urlPrix+ut)

    # print(allUrls)
    res = []
    for u in allUrls:
        urls = parseUrl(u,'//div[@class="index_left"]/ul/li/a/@href')[1]

        for u in urls:
            res.append(urlPrix+u)
    return res

def containTag(url,tag):
    result = False
    elementTags = parseUrl(url,'//div[@class="main"]/div[1]/div[1]/div[2]/div[3]/p[2]/a')[1]
    for elementTag in elementTags:
        if elementTag.text is None:
            continue
        result = elementTag.text.find(tag) != -1
        if result:
            break
    return result



if __name__ == '__main__':
    list = [

        # 'http://www.quantuwang.cc/t/e4d09316d8a9d330.html', #小热巴
        # 'http://www.quantuwang.cc/t/6f8fbb7c34c9bf4f.html', # 柳侑绮
        # 'http://www.quantuwang.cc/t/956ac07ef794d061.html',# 艾小青
        # 'http://www.quantuwang.cc/t/584f16e805c0ecc3.html',#赵小米
        # 'http://www.quantuwang.cc/t/a770ab3955dfecd5.html',#夏美酱
        # 'http://www.quantuwang.cc/t/402660ed007a8bb2.html',#薛琪琪
        # 'http://www.quantuwang.cc/t/aca6a5b5e8c338c9.html',#杨紫嫣
        # 'http://www.quantuwang.cc/t/95116806adafed5f.html',#七七
        # 'http://www.quantuwang.cc/t/b4581a982e96eae7.html',#艾栗栗
        # 'http://www.quantuwang.cc/t/15c3767f8a07de21.html',# 陆萱萱
        # 'http://www.quantuwang.cc/t/a5196f36e26bb71c.html',#沈梦瑶
        # 'http://www.quantuwang.cc/t/9987f205a66cb83f.html',#方子萱
        'http://www.quantuwang.cc/t/0fe398c14ee967d6.html',#就是阿朱啊
        'http://www.quantuwang.cc/t/48bada5e7225ec9f.html',#杨晨晨
        'http://www.quantuwang.cc/t/4eba90c841ec7445.html',#林文文
        'http://www.quantuwang.cc/t/de6bdb42ece2255f.html',#周于希
        'http://www.quantuwang.cc/t/b46b8da68451464e.html',#玥儿玥
        'http://www.quantuwang.cc/t/fc1868c8a652655f.html',#果儿
        # 'http://www.quantuwang.cc/t/6a5d00e535915ee5.html',#王雨纯
        # 'http://www.quantuwang.cc/t/f4543e3a7d545391.html',  # 糯美子Mini
        'http://www.quantuwang.cc/meinv/xiuren/',
        'http://www.quantuwang.cc/meinv/mygirl/',
        'http://www.quantuwang.cc/meinv/mfstar/',
        'http://www.quantuwang.cc/meinv/feilin/',
        'http://www.quantuwang.cc/meinv/huayan/'
    ]
    for l in list:
        urlsByName = getAllUrlsByName(l,'http://www.quantuwang.cc/')
        # print(urlsByName )
        for urlName in urlsByName:
            loadExecutor.submit(load,urlName)



