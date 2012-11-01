from tucarro.items import Carro
from scrapy.selector.lxmlsel import HtmlXPathSelector
from scrapy.contrib.spiders.crawl import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


#Arania que escrapea los carros renault de tu carro usando CrawlSpider
class TuCarroCrawlSpider(CrawlSpider):
    start_urls = ['http://listado.tucarro.com.ve/carros/renault/']
    allowed_domains = ['listado.tucarro.com.ve', 'articulo.tucarro.com.ve']
    name = 'tucarro_crawl'

    rules = [
             Rule(SgmlLinkExtractor(".*MLV.*"), 'parse_carro'),
             Rule(SgmlLinkExtractor(".*_Desde.*"), 'parse'),

            ]

    def parse_carro(self, response):
        hxs = HtmlXPathSelector(response)
        carro = Carro()
        carro['modelo'] = hxs.select('//div[@class="section primary"]/h1/text()').extract()[0]
        anio, tipo = hxs.select('//div[@class="section primary"]/h4/text()').extract()[0].split("|")
        carro['anio'] = anio
        carro['tipo'] = tipo
        carro['precio'] = hxs.select('//div[@class="section primary"]/h3/text()').extract()[0].split(" ")[-1]
        carro['url'] = response.url
        yield carro
