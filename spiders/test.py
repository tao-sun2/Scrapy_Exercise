# -*- coding: utf-8 -*-
import scrapy

from demo.items import DemoItem


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base = "https://www.qiushibaike.com"

    def parse(self, response):

        contents = response.xpath("//div[@class='col1 old-style-col1']/div")
        for c in contents:
            authors = c.xpath(".//h2/text()").get().strip()
            cc = c.xpath(".//div[@class='content']//text()").getall()
            cc = "".join(cc).strip()
            print(authors)
            print(cc)
            items = DemoItem(author=authors, content=cc)
            yield items
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()

        if not next_url:
            print(next_url)
            print(response)
            return
        else:
            print(next_url)
            yield scrapy.Request(self.base + next_url, callback=self.parse)
