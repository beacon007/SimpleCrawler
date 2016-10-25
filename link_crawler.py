#coding:utf-8
import re,urlparse
from downloader import Downloader

class LinkCrawler():
    """给定一个种子连接，返回匹配的url"""
    def __init__(self, seed_url,url_pattern,max_depth=0):
        self.downloader = Downloader()
        self.seed_url = seed_url
        self.url_pattern = url_pattern
        self.max_depth = max_depth

    def link_crawler(self):
        crawl_queue = [self.seed_url]
        # keep track which URL's have seen before
        seen = set(crawl_queue)
        depth = 0
        links = []
        while depth<=self.max_depth and crawl_queue:
            url = crawl_queue.pop()
            html = self.downloader.download(url)
            for link in self.get_links(html):
                # check if link matches expected regex
                if re.match(self.url_pattern, link):
                    # form absolute link
                    link = urlparse.urljoin(self.seed_url, link)
                    # check if have already seen this link
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
                        links.append(link)
                        print(link)
            depth+=1
        return links

    def get_links(self,html):
        """Return a list of links from html
        """
        # a regular expression to extract all links from the webpage
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        # list of all links from the webpage
        return webpage_regex.findall(html)

if __name__ == "__main__":
    #LinkCrawler("http://www.bing.com","http",1).link_crawler()
    LinkCrawler("http://www.zhihu.com/topic/19552207/hot","/question/\d+$").link_crawler()
