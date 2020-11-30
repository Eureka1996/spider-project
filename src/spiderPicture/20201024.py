# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import urllib.parse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os
import string

loadExecutor = ThreadPoolExecutor(max_workers=25)
localPath = 'D:\\MyDrivers\\update\\photo5'


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
    filenameTmp = '%s\\%s' % (localPath,filename)
    try:
        if not os.path.exists(filenameTmp):
            print('\t\t(%d,%d,%d)下载图片%d：%s,%s'%(pictureIndex[0],pictureIndex[1],pictureIndex[2],reLoadTime,filename,url))
            pictureContent = urllib.request.urlopen(url,timeout=120).read()
            with open(filenameTmp, "wb") as f:
                f.write(pictureContent)
            print('\t\t(%d,%d,%d)下载图片完成：%s' % (pictureIndex[0], pictureIndex[1],pictureIndex[2], filename))
        else:
            print('\t\t(%d,%d,%d)图片已经存在：%s' % (pictureIndex[0], pictureIndex[1],pictureIndex[2], filename))
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

    print(allUrls)
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
        'http://www.quantuwang.cc/t/15c3767f8a07de21.html',
        'http://www.quantuwang.cc/t/a5196f36e26bb71c.html',
        'http://www.quantuwang.cc/t/6a5d00e535915ee5.html',
        'http://www.quantuwang.cc/t/9987f205a66cb83f.html',
        'http://www.quantuwang.cc/t/0fe398c14ee967d6.html',
        'http://www.quantuwang.cc/meinv/xiuren/',
        'http://www.quantuwang.cc/meinv/mygirl/',
        'http://www.quantuwang.cc/meinv/mfstar/',
        'http://www.quantuwang.cc/meinv/feilin/',
        'http://www.quantuwang.cc/meinv/huayan/'
    ]
    for l in list:
        urlsByName = getAllUrlsByName(l,'http://www.quantuwang.cc/')
        print(urlsByName )
        for urlName in urlsByName:
            loadExecutor.submit(load,urlName)



