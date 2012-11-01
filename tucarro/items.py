from scrapy.item import Item, Field


# Esta clase representa el item que queremos extraer
class Carro(Item):
    modelo = Field()
    anio = Field()
    tipo = Field()
    precio = Field()
    url = Field()
