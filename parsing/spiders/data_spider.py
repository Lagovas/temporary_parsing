# coding: utf-8
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from parsing.items import ParsingItem


class DataSpider(CrawlSpider):
    name = "data spider"
    allowed_domains = [os.environ.get('PARSE_DOMAIN')]
    start_urls = [
        "https://{}/catalog/".format(os.environ.get('PARSE_DOMAIN'))
    ]

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(restrict_xpaths=['/html/body/main/section/div/div[2]/ul/li/a'],
                           restrict_css=['body > main > section:nth-child(3) > div > ul > li > a'])),

        Rule(LinkExtractor(restrict_css=['body > main > section > div > div.result-list > div > a']),
             callback='parse_data'),
    )
    content_map = {
        u'ФОП': 'name',
        u'Місто': 'city',
        u'Адреса': 'address',
        u'Телефон': 'phone'
    }

    def parse_data(self, response):
        content_items = response.xpath('/html/body/main/section/div/div/div')
        item = {}
        for content_item in content_items:
            title = content_item.xpath('div[1]/text()').extract_first()
            value = content_item.xpath('div[2]/text()').extract_first()
            item[self.content_map[title]] = value
        yield ParsingItem(**item)
