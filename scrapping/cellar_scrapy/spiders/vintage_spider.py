import scrapy
import json
from scrapy.loader import ItemLoader
from scrapping.cellar_scrapy.items import VintageItem

class VintageSpider(scrapy.Spider):
    name="vintage"

    def __init__(self, query='', *args, **kwargs):
        super(VintageSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=fr&source=gcsc&gss=.fr&cselibv=57975621473fd078&cx=partner-pub-2369878421197151:3543362435&q={}%20mill%C3%A9sime&safe=active&cse_tok=AJvRUv1poVztdGezzJwiHZ_E-2_g:1588751040554&exp=csqr,cc&callback=google.search.cse.api9550'.format(query[0])]
        self.area_name = query[1]

    def parse(self, response):
        res = json.loads(response.text[34:-2])
        for r in res['results']:
            test = r['url'].split('/')
            if test[3] == 'millesimes':
                if test[-1][:3] == 'vin':
                    return response.follow(r['url'], callback=self.parse_vin)
                elif test[-1][:3]=='app':
                    return response.follow(r['url'], callback=self.parse_area)

    def parse_area(self, response):
        types = response.css('table.contenu tr:nth-child(5) tr')
        for i,res in enumerate(types):
            if i in [4,6,8,10]:
                color = response.css('table.contenu tr:nth-child(5) tr:nth-child({}) h3::text'.format(i)).get()
                if color or i==4:
                    ranks = response.css('table.contenu tr:nth-child(5) tr:nth-child({}) td table tr'.format(i+1))
                    for j,rank in enumerate(ranks):
                        if j!=0:
                            loader = ItemLoader(item=VintageItem(), selector=rank)
                            loader.add_css('rank', css='strong::text')
                            loader.add_css('years', css='td::text')
                            loader.add_css('years', css='a::text')
                            loader.add_value('color',color)
                            loader.add_value('area_name',self.area_name)
                            yield loader.load_item()

    def parse_vin(self, response):
        ranks = response.css('table.contenu tr:nth-child(5) table tr:nth-child(3) table tr')
        for j,rank in enumerate(ranks):
            if j!=0:
                loader = ItemLoader(item=VintageItem(), selector=rank)
                loader.add_css('rank', css='strong::text')
                loader.add_css('years', css='td::text')
                loader.add_css('years', css='a::text')
                loader.add_value('area_name',self.area_name)
                yield loader.load_item()

