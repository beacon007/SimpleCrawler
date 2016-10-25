#coding: utf-8
import urllib,os
import lxml.html.soupparser as sp
import threading,thread
from link_crawler import LinkCrawler
from downloader import Downloader

class ThreadCrawler(threading.Thread):
    def __init__(self, html):
        threading.Thread.__init__(self)
        self.html = html
        # 调用父类构造函数

    def run(self):
        # 重写run()函数，线程默认从此函数开始执行
        get_images_from_zhihu(self.html)

def zhihu_img_crawler(url_from_zhihu):

    for link in LinkCrawler(url_from_zhihu,"/question/\d+$").link_crawler():
        ThreadCrawler(Downloader().download(link)).start()



def get_images_from_zhihu(html):
    print threading.currentThread().getName()
    dom = sp.fromstring(html)
    print threading.currentThread().getName()
    for img_link in dom.xpath('//*[@id="zh-question-answer-wrap"]//img[@data-original]/@data-original'):
        #print("Get img_link :  " + img_link)
        store_image(img_link, img_link[23:])

def store_image(url, filename):
    path = os.path.abspath(IMAGE_PATH)
    if not os.path.exists(path):
        os.mkdir(path)
    dest_dir = os.path.join(path, filename)
    if not os.path.exists(dest_dir):
        #print ("Downloading...")
        urllib.urlretrieve(url, dest_dir)

# def is_pretty_girl(html):
#     dom = sp.fromstring(html)
#     key_words = [u"\n\u7f8e\u5973\n"]
#     for key_word in key_words:
#         if key_word in dom.xpath('//*[@class="zm-tag-editor-labels zg-clear"]//a/text()'):
#             return True

IMAGE_PATH="zhihu_images/"

if __name__=="__main__":
    # links=LinkCrawler("https://www.zhihu.com/topic/19552207/hot", "/question/\d+$").link_crawler()
    # ThreadCrawler(Downloader().download(links[0])).start()
    # ThreadCrawler(Downloader().download(links[1])).start()
    # ThreadCrawler(Downloader().download(links[2])).start()
    # ThreadCrawler(Downloader().download(links[3])).start()
    # ThreadCrawler(Downloader().download(links[4])).start()
    zhihu_img_crawler("https://www.zhihu.com/topic/19552207/hot")




