# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Subject(Item):
    # define the fields for your item here like:
    # name = Field()
    id = Field()
    title = Field()
    speakers = Field()

class Speaker(Item):
    name = Field()
    group = Field()
    canton = Field()
    detailPage = Field()