# -*- coding: utf-8 -*-

import socket
import urllib.request
import urllib.error
import urllib.parse
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os


def loadPicture(url,localPath,filename):
    filenameTmp = localPath+'/'+filename
    try:
        if os.path.exists(filenameTmp):
            print(filenameTmp+"已经存在")
        else:
            print('保存图片：' + url+"->"+filenameTmp)
            pictureContent = urllib.request.urlopen(url,timeout=20).read()
            with open(filenameTmp, "wb") as f:
                f.write(pictureContent)
            # urllib.request.urlretrieve(url, filename=localPath + '/' + filename)
    except Exception as e:
        loadPicture(url,localPath,filename)


def crawPictureUrl(url):
    html = urllib.request.urlopen(url).read()
    html = etree.HTML(html)

    divCount = 2
    pictureNames = html.xpath('//div[@class="main"]/div['+str(divCount)+']/a/@title')
    if len(pictureNames) == 0 :
        divCount = 3
        pictureNames = html.xpath('//div[@class="main"]/div[' + str(divCount) + ']/a/@title')

    pictureName = pictureNames[0]
    pictureUrls = html.xpath('//div[@class="main"]/div['+str(divCount)+']/a/img/@src')

    for pictureUrl in pictureUrls:
        print("pictureUrl:"+pictureUrl)
        filename = str(pictureName) + pictureUrl[str(pictureUrl).rfind('/')+1:]
        loadPicture(pictureUrl, './photo', filename)
    pageCount = divCount + 1
    pageColumn = html.xpath('//div[@class="main"]/div['+str(pageCount)+']/a[last()-1]')

    if len(pageColumn) == 0:
        pageCount+=1
        pageColumn = html.xpath('//div[@class="main"]/div['+str(pageCount)+']/a[last()-1]')

    pictureCount = pageColumn[0].text
    preUrl = url[:url.rfind('.')]
    for i in range(2,int(pictureCount)+1):
        newUrl = preUrl+"_"+str(i)+".html"
        print(pictureCount+','+newUrl)
        newHtml = urllib.request.urlopen(newUrl).read()
        newHtml = etree.HTML(newHtml)
        pictureUrls = newHtml.xpath('//div[@class="main"]/div['+str(divCount)+']/a/img/@src')
        for pictureUrl in pictureUrls:
            filename = str(pictureName) + pictureUrl[str(pictureUrl).rfind('/') + 1:]
            loadPicture(pictureUrl, './photo', filename)

    return pictureName,pictureUrls

def crawIndexPage(url):
    indexPageContent = urllib.request.urlopen(url).read()
    indexPageHtml = etree.HTML(indexPageContent)
    indexPagePictureUrls = indexPageHtml.xpath('//div[@class="index_list"]/div[@class="index_pic"]/ul/li/a/@href')
    return indexPagePictureUrls

if __name__ == '__main__':
    preUrl = 'http://www.9900rt.org/html/yazhou/'
    website = 'http://www.9900rt.org/'
    executor = ThreadPoolExecutor(max_workers=20)
    for i in range(1,188):
        url = ''
        if i == 1:
            url = preUrl
        else:
            url = preUrl + str(i)+'.html'

        indexPagePictureUrls = crawIndexPage(url)
        for indexPagePictureUrl in indexPagePictureUrls:
            indexPagePictureUrl = website + indexPagePictureUrl
            executor.submit(crawPictureUrl,indexPagePictureUrl)
