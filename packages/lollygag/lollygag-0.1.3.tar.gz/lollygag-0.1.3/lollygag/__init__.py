from lollygag.services import register_services
from lollygag.crawler.domain_crawler import DomainCrawler

def run(**kwargs):
    register_services()
    crawler = DomainCrawler() if "crawler" not in kwargs else kwargs["crawler"]
    url = None if "url" not in kwargs else kwargs["url"]
    crawler.crawl_domain(url)
