# coding: utf-8
import scrapy

class QuoteSpider(scrapy.Spider): # 自己定义的类继承自scrapy.Spider
    'defines some attributes and methods'
    name = 'quotes1' # unique

    def start_requests(self):
        '''return an iterable of Requests.
        Subsequent requests will be generated successively from these initial requests.'''
        urls = [
            'http://quotes.toscrape.com/page/1/',
            # 'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) # 返回scrapy.Request对象
    # def parse(self, response):
    #     '''parses the response, extracting the scraped data as dicts
    #     and also finding new URLs to follow and creating new requests (Request) from them.'''
    #     page = response.url.split('/')[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('saved file % s' % filename)
    #     # 网页被下载下来了
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small.author::text').extract_first(),
                'tags' : quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()  # 两级标签提取内容

        if next_page is not None:
            next_page = response.urljoin(next_page)  # 创建绝对路径
            yield scrapy.Request(next_page, callback=self.parse)  # 回调函数，递归处理



# 默认情况下，可以不用初始请求
'''
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
'''