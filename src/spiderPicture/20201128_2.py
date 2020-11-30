# -*- coding: utf-8 -*-

import urllib.request
import urllib.error
import urllib.parse
# import lxml.html
from lxml import html
# from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import os
import shutil

etree = html.etree
loadExecutor = ThreadPoolExecutor(max_workers=50)
localPath = 'D:\\MyDrivers\\update\\photo5'

def getPictureLink(url):
    name = parseUrl(url, '//div[@class="c_title"]/h1[1]/text()')[1]
    personName = parseUrl(url,'//div[@class="c_tag"]/p/a[1]/text()')[1]
    links = parseUrl(url, '//div[@class="c_img"]/a[1]/img[1]/@src')[1]
    return (name[0].replace("/",""),links[0],personName[0])

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

def loadPicture(url,localPath,filename,personName,pictureIndex,reLoadTime):
    # print(personName)
    if reLoadTime > 5:
        return


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



def load(urlName):
    urls = crawPictureSetUrls(urlName, 'http://www.quantuwang.cc/')
    for url in urls:
        link = getPictureLink(url)
        loadPicture(link[1], localPath, link[0] + '.jpg',link[2], (0, 0, 1), 0)



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
        # 'http://www.quantuwang.cc/t/0fe398c14ee967d6.html',#就是阿朱啊
        # 'http://www.quantuwang.cc/t/48bada5e7225ec9f.html',#杨晨晨
        # 'http://www.quantuwang.cc/t/4eba90c841ec7445.html',#林文文
        # 'http://www.quantuwang.cc/t/de6bdb42ece2255f.html',#周于希
        # 'http://www.quantuwang.cc/t/b46b8da68451464e.html',#玥儿玥
        # 'http://www.quantuwang.cc/t/fc1868c8a652655f.html',#果儿
        # 'http://www.quantuwang.cc/t/6a5d00e535915ee5.html',#王雨纯
        # 'http://www.quantuwang.cc/t/f4543e3a7d545391.html',  # 糯美子Mini
        # 'http://www.quantuwang.cc/meinv/leyuan/',#星乐园
        # 'http://www.quantuwang.cc/meinv/miitao/',#蜜桃社
        'http://www.quantuwang.cc/meinv/mistar/',#魅妍社
        'http://www.quantuwang.cc/meinv/tgod/',#推女神
        'http://www.quantuwang.cc/meinv/youmi/',# 尤蜜荟
        'http://www.quantuwang.cc/meinv/xiaoyu/',#语话界
        # 'http://www.quantuwang.cc/meinv/imiss/',#爱蜜社
        # 'http://www.quantuwang.cc/meinv/huayan/',  # 花の颜

        # 'http://www.quantuwang.cc/meinv/mygirl/',#美媛馆
        # 'http://www.quantuwang.cc/meinv/mfstar/',# 模范学院
        # 'http://www.quantuwang.cc/meinv/feilin/',#嗲囡囡
        'http://www.quantuwang.cc/meinv/xiuren/'  # 秀人网
    ]
    for l in list:
        urlsByName = getAllUrlsByName(l,'http://www.quantuwang.cc/')
        # print(urlsByName )
        for urlName in urlsByName:
            loadExecutor.submit(load,urlName)



