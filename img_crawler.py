import urllib,os
import lxml.html.soupparser as sp
from link_crawler import LinkCrawler
from downloader import Downloader

def zhihu_img_crawler(url_from_zhihu):
    for link in LinkCrawler(url_from_zhihu,"/question/\d+$").link_crawler():
        get_images_from_zhihu(Downloader().download(link))

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


IMAGE_PATH="zhihu_images/"

if __name__=="__main__":
    zhihu_img_crawler("http://www.zhihu.com/topic/19552207/hot")
