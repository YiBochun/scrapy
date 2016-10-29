# coding: utf-8
'''
Scrapy is an application framework for crawling web sites and extracting structured data which can be used for a wide
range of useful applications, like data mining, information processing or historical archival.it can also be used to
extract data using APIsor as a general purpose web crawler.
scheduled and processed asynchronously.
Thismeans that Scrapy doesn’t need to wait for a request to be finished and processed, it can send another request or do
other things in the meantime. This also means that other requests can keep going even if some request fails or an error
happens while handling it.
'''
'''
an example 'http://quotes.toscrape.com'
'''
import scrapy

class QuotesSpider(scrapy.Spider):
    'name唯一,start_urls为地址列表，记得最后添加逗号'
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/tag/humor/',]

    def parse(self, response):
        '将response作为参数传递给parse方法'
        for quote in response.css('div.quote'):
            # 审查元素得知div是定位内容的一级标签，quote是class属性值
            yield {
                # text、author都是class属性值
                # 抽取内容方法，css、xpath
                'text' : quote.css('span.text::text').extract_first(),
                'author' : quote.xpath('span/small/text()').extract_first(),
            }
        # 找到下一页标签
        next_page = response.css('li.next a::attr("href")').extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page) #生成绝对路径
            yield scrapy.Request(next_page, callback=self.parse) # 回调函数，递归。
            # 在命令行下，定位到爬虫所在目录，执行scrapy runspider quotes_spider.py -o quotes.json，
            # 注意文件名是爬虫类的小写且没有中间下划线，以json或者csv等格式输出。