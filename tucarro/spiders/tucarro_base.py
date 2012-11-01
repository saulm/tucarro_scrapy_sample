from scrapy.spider import BaseSpider
from tucarro.items import Carro
from scrapy.selector.lxmlsel import HtmlXPathSelector
from scrapy.http.request import Request


#Arania que escrapea los carros renault de tu carro usando BaseSpider
class TuCarroBaseSpider(BaseSpider):
    start_urls = ['http://listado.tucarro.com.ve/carros/renault/']
    allowed_domains = ['listado.tucarro.com.ve']
    name = 'tucarro_base'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        car_lis = hxs.select('//li[@class="standard_200 t gal-normal-mot"]')
        #Parsear cada li de carro
        for li in car_lis:
            carro = Carro()
            carro['modelo'] = li.select('div/h3/a/text()').extract()[0]
            anio, tipo = li.select('div[@class="itemInfo"]//h4/strong/text()').extract()[0].split("|")
            carro['anio'] = anio
            carro['tipo'] = tipo
            carro['precio'] = li.select('div[@class="itemInfo"]//li[@class="precio_gal"]/strong/text()'
                                        ).extract()[0].split(" ")[-1]
            carro['url'] = li.select('div/h3/a/@href').extract()[0]
            yield carro

        url_paginas = hxs.select("//div[@id='paginador']/a/@href").extract()
        for pagina in url_paginas:
            yield(Request(pagina, callback=self.parse))
