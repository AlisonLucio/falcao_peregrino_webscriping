import scrapy


class EmendasParlamentaresSpider(scrapy.Spider):
    name = "emendas_parlamentares"
    path_origin = 'https://dados.gov.br/dataset/emendas-parlamentares'

    start_urls = [
        path_origin
    ]

    ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}

    def parse(self, response):
        links = response.xpath('.//*[@id="dataset-resources"]/ul/li[*]/a')
        f = open('teste.txt', 'a')

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
        print('==================== parse_download linha 33')
        f = open('teste_2.txt', 'a')
        link_file = response.urljoin(response.xpath('.//*[@id="content"]/div[3]/section/div[1]/p/a/@href').get())
        dict_link = {'href_file': link_file}

        f.write(f'\n {dict_link}')
        print('==================== parse_download linha 39')

        yield dict_link





