#coding: utf-8
import urllib,os
import lxml.html.soupparser as sp
import threading
from link_crawler import LinkCrawler
from downloader import Downloader


def zhihu_img_crawler(url_from_zhihu):
    if not os.path.exists(IMAGE_PATH):
        os.mkdir(IMAGE_PATH)
    for link in LinkCrawler(url_from_zhihu,"/question/\d+$").link_crawler():
        get_images_from_zhihu(Downloader().download(link),10)



def get_images_from_zhihu(html,max_threads):
    dom = sp.fromstring(html)
    """单线程"""
    # for img_link in dom.xpath('//*[@id="zh-question-answer-wrap"]//img[@data-original]/@data-original'):
    #     print("Get img_link :  " + img_link)
    #     store_image(img_link)
    """多线程"""
    links = dom.xpath('//*[@id="zh-question-answer-wrap"]//img[@data-original]/@data-original')
    threads = []
    while threads or links:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and links:
            link = links.pop()
            print("Get img_link :  " + link)
            thread = threading.Thread(store_image(link))
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

def store_image(url):
    path = os.path.abspath(IMAGE_PATH)
    dest_dir = os.path.join(path, url[23:])
    if not os.path.exists(dest_dir):
        print ("Downloading img...")
        urllib.urlretrieve(url, dest_dir)



IMAGE_PATH="zhihu_images/"

if __name__=="__main__":

    zhihu_img_crawler("https://www.zhihu.com/topic/19552207/top-answers")



