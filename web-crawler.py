import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.url_count = 0

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            #TODO: check if the link tag has the rb-plp-product-tile value in the attribute class
            if 'rb-plp-product-tile' in link.get('class'):
                path = link.get('href')
                if path and path.startswith('/'):
                    path = urljoin(url, path)
                yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    # Do the actual crawling of the webpage
    def crawl(self, url):
        self.url_count += 1
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)

if __name__ == '__main__':
    Crawler(urls=['https://www.ray-ban.com/usa/sunglasses/view-all']).run()
