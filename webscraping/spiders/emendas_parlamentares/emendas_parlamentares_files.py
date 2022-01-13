import scrapy


class DownloaderItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
