import scrapy
from scrapy.loader import ItemLoader

from webscraping.spiders.emendas_parlamentares.emendas_parlamentares_files import DownloaderItem


class EmendParlaSpider(scrapy.Spider):
    name = "emendasParlamentaresSpider"
    path_origin = 'https://dados.gov.br/dataset/emendas-parlamentares'
    path_url_link_files = 'source/emendas_parlamentares/'

    start_urls = [
        path_origin
    ]

    def parse(self, response):
        links = response.xpath('.//*[@id="dataset-resources"]/ul/li[*]/a')
        f = open(f'{self.path_url_link_files}url_files.txt', 'a')

        for link in links:
            dict_link = {
                'title': link.xpath('./@title').get(),
                'href_page': response.urljoin(link.xpath('./@href').get()),
                'data_format': link.xpath('.//@data-format').get()
            }
            f.write(f'\n {dict_link}')

            next_page = dict_link['href_page']

            if next_page is not None:
                yield scrapy.Request(url=next_page, callback=self.parse_download)

    def parse_download(self, response):
        f = open(f'{self.path_url_link_files}url_download_files.txt', 'a')

        selector = './/*[@id="content"]/div[3]/section/div[1]/p/a/@href'
        absolute_url = response.urljoin(response.xpath(selector).get())
        loader = ItemLoader(item=DownloaderItem(), selector=selector)
        loader.add_value('file_urls', absolute_url)

        dict_link = {'href_file': absolute_url}
        f.write(f'\n {dict_link}')

        yield loader.load_item()
