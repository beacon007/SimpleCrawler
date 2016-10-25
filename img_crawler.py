import urllib,os,time
import lxml.html.soupparser as sp
import threading
from link_crawler import LinkCrawler
from downloader import Downloader

def zhihu_img_crawler(url_from_zhihu,max_threads=10):
    threads = []
    links = LinkCrawler(url_from_zhihu,"/question/\d+$").link_crawler()
    while threads or links:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and links:
            # can start some more threads
            thread = threading.Thread(target=get_images_from_zhihu(Downloader().download(links.pop())))
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        # all threads have been processed
        # sleep temporarily so CPU can focus execution elsewhere
        time.sleep(SLEEP_TIME)


def get_images_from_zhihu(html):
    path = os.path.abspath(IMAGE_PATH)
    if not os.path.exists(path):
        os.mkdir(path)
    dom = sp.fromstring(html)
    for img_link in dom.xpath('//*[@id="zh-question-answer-wrap"]//img[@data-original]/@data-original'):
        print("Get img_link :  " + img_link)
        store_image(img_link, path, img_link[23:])

def store_image(url, path, filename):
    print ("Downloading...")
    dest_dir = os.path.join(path, filename)
    if not os.path.exists(dest_dir):
        urllib.urlretrieve(url, dest_dir)

# def is_pretty_girl(html):
#     dom = sp.fromstring(html)
#     key_words = [u"\n\u7f8e\u5973\n"]
#     for key_word in key_words:
#         if key_word in dom.xpath('//*[@class="zm-tag-editor-labels zg-clear"]//a/text()'):
#             return True

SLEEP_TIME=1
IMAGE_PATH="zhihu_images/"

if __name__=="__main__":
    zhihu_img_crawler("http://www.zhihu.com/topic/19552207/hot")
