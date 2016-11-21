#coding: utf-8
import urllib,os
import lxml.html.soupparser as sp
import thread,threading
from link_crawler import LinkCrawler
from downloader import Downloader


def zhihu_img_crawler(url_from_zhihu):
    if not os.path.exists(IMAGE_PATH):
        os.mkdir(IMAGE_PATH)
    for link in LinkCrawler(url_from_zhihu,"/question/\d+$").link_crawler():
        get_images_from_zhihu(Downloader().download(link))



def get_images_from_zhihu(html):
    dom = sp.fromstring(html)
    for img_link in dom.xpath('//*[@id="zh-question-answer-wrap"]//img[@data-original]/@data-original'):
        print("Get img_link :  " + img_link)
        if (threading.enumerate().__len__()<5):
            thread.start_new_thread(store_image,(img_link,img_link[23:]))


def store_image(url, filename):
    path = os.path.abspath(IMAGE_PATH)
    dest_dir = os.path.join(path, filename)
    if not os.path.exists(dest_dir):
        print ("Downloading img...")
        urllib.urlretrieve(url, dest_dir)



IMAGE_PATH="zhihu_images/"

if __name__=="__main__":
    # links=LinkCrawler("https://www.zhihu.com/topic/19552207/hot", "/question/\d+$").link_crawler()
    # ThreadCrawler(Downloader().download(links[0])).start()
    # ThreadCrawler(Downloader().download(links[1])).start()
    # ThreadCrawler(Downloader().download(links[2])).start()
    # ThreadCrawler(Downloader().download(links[3])).start()
    # ThreadCrawler(Downloader().download(links[4])).start()
    zhihu_img_crawler("https://www.zhihu.com/topic/19552207/hot")



