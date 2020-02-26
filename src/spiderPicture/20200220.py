# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import urllib.parse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os
import string

# pictureUrlExecutor = ThreadPoolExecutor(max_workers=5)
loadExecutor = ThreadPoolExecutor(max_workers=25)
localPath = 'D:\\MyDrivers\\update\\photo'

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

def load(url,pictureSetDesc,pictureIndex):
    pictureDivCount = 2
    parseUrlResult = parseUrl(url,'//div[@class="main"]/div['+str(pictureDivCount)+']/a/img/@src')
    pictureSrcs = parseUrlResult[1]
    while len(pictureSrcs) == 0:
        pictureDivCount+=1
        pictureSrcs = parseUrlResult[0].xpath('//div[@class="main"]/div[' + str(pictureDivCount) + ']/a/img/@src')

    for pictureSrc in pictureSrcs:
        filename = getFilename(pictureSrc, pictureSetDesc[0])
        pictureCount = pictureSetDesc[1]
        loadPicture(pictureSrc,localPath,filename,(pictureIndex[0],pictureIndex[1],int(pictureCount)),0)



def crawPictureUrl(url,pictureIndex):

    pictureSetDesc = getPictureSetDesc(url)

    preUrl = url[:url.rfind('.')]
    for i in range(1,int(pictureSetDesc[1])+1):
        pictureUrl = url
        if i != 1:
            pictureUrl = preUrl + "_" + str(i) + ".html"
        # print('pictureUrl:%s'%pictureUrl)
        loadExecutor.submit(load,pictureUrl,pictureSetDesc,pictureIndex)
        # load(pictureUrl,pictureSetDesc,pictureIndex)

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



def main():
    preUrl = 'http://www.9900rt.org/html/yazhou/'
    website = 'http://www.9900rt.org/'

    for i in range(40,188):
        url = ''
        if i == 1:
            url = preUrl
        else:
            url = preUrl + str(i)+'.html'

        indexPagePictureUrls = []
        while len(indexPagePictureUrls) == 0:
            indexPagePictureUrls = parseUrl(url,'//div[@class="index_list"]/div[@class="index_pic"]/ul/li/a/@href')[1]
        count = 0
        for indexPagePictureUrl in indexPagePictureUrls:
            count+=1;
            print("(%d,%d)"%(i,count))
            indexPagePictureUrl = website + indexPagePictureUrl
            # 判断是否包含指定的标签
            isContainTag = containTag(indexPagePictureUrl,'日本')
            if not isContainTag:
                print('\t(%d,%d)爬取图片链接：%s'%(i,count,indexPagePictureUrl))
                crawPictureUrl(indexPagePictureUrl,(i,count))

def main2():
    urls = [
        'http://www.9900rt.info/html/yazhou/2016/0805/4355.html',
        'http://www.9900rt.info/html/yazhou/2017/0921/5913.html',
        'http://www.9900rt.info/html/yazhou/2017/1015/5997.html'
    ]

    for url in urls:
        crawPictureUrl(url, (0, 0))

if __name__ == '__main__':
    main()