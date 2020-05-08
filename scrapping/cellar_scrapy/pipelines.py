# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time
from .models.area import Area, AreaInfo, AreaGrape, Grape, GrapeSynonym, AreaVintage
from .models.region import Region, RegionInfo
from .models.recipe import Category, Recipe, AreaRecipe


from playhouse.postgres_ext import PostgresqlExtDatabase
# from peewee import PostgresqlDatabase
from urllib.parse import urlparse

class WineDeciderPipeline(object):
    items = []
    is_running = False
    start_time = 0
    last_query = ''

    def __init__(self):
        WineDeciderPipeline.items = []
        self.ids_seen = set()
        WineDeciderPipeline.is_running = True
        
    def process_item(self, item, spider):
        int_result = {}
        for key in item.keys():
            if key!='maturity':
                int_result[key] = item[key]
            else:
                color,maturity = item[key].split('/')
                int_result['color'] = color
                int_result['maturity'] = maturity
        WineDeciderPipeline.items.append(int_result)      

class HachettePipeline(object):
    items = []

    def __init__(self):
        HachettePipeline.items = []
    def process_item(self, item, spider):
        int_result = {}

        # vintage_list = re.findall(r'[0-9]{4,}',item['wine_name'])
        # if len(vintage_list) > 0:
        #     int_result['vintage'] = vintage_list[0]
        #     item['wine_name'] = item['wine_name'].strip(vintage_list[0])
        for key in item.keys():
            int_result[key] = item[key]
        if int_result['wine_name'] == '':
            int_result['wine_name'] = item['default_name']
        HachettePipeline.items.append(int_result)
        
class RecipePipeline(object):
    def process_item(self, item, spider):
        int_result = {}
        for key in item.keys():
            int_result[key] = item[key]
        RecipePipeline.items = int_result

class RecipesPipeline(object):

    def __init__(self):
        no_category = Category.get_or_none(name='no category')
        if not no_category:
            Category.create(name='no category')

    def process_item(self, item, spider):
        print(item)
        # update the existing recipes
        recipe = Recipe.get_or_none(name=item['name'])
        if recipe:
            true_item = {
                'name':'',
                'ingredients':'',
                'image':'',
                'desc':'',
                'preparation':'',
                'proportion':'',
                'time_prep':'',
                'time_cook':'',
            }
            for key in item.keys():
                true_item[key] = item[key]
            Recipe.update(
                image=true_item['image'],
                proportion=true_item['proportion'],
                preparation=true_item['preparation'],
                time_prep=true_item['time_prep'],
                time_cook=true_item['time_cook'],
                description=true_item['desc'],
            ).where(Recipe.id==recipe.id).execute()
        else:
            # Import and create all recipes
            if 'category_name' in item.keys():
                category = Category.get_or_none(name=item['category_name'])
                if not category:
                    category = Category.create(name=item['category_name'])
            else:
                category = Category.get_or_none(name='no category')
            true_item = {
                'name':'',
                'ingredients':'',
                'image':'',
                'desc':'',
                'preparation':'',
                'proportion':'',
                'time_prep':'',
                'time_cook':'',
            }
            for key in item.keys():
                true_item[key] = item[key]
            recipe = Recipe.create(category=category, description=true_item['desc'], **true_item)
            for area_name in item['areas']:
                area = Area.get_or_none(name=area_name)
                if not area:
                    area = Area.create(name=area_name)
                area_recipe = AreaRecipe.get_or_none(area=area, recipe=recipe)
                if not area_recipe:
                    AreaRecipe.create(area=area, recipe=recipe)

class WinePipeline(object):
    items = None

    def __init__(self):
        WinePipeline.items = None
        self.ids_seen = set()

    def process_item(self, item, spider):
        int_result = {}
        int_result['recipes'] = {}
        for key in item.keys():
            if key in ['recipes_names', 'recipes_urls']:
                int_result['recipes'][key] = item[key]
            else:
                int_result[key] = item[key]
        WinePipeline.items = int_result

class RegionPipeline(object):

    def process_item(self, item, spider):
        # uncomment to add photo of the region in the db

        if 'region_name' in item.keys():
            print(item)
            region = Region.get_or_none(name=item['region_name'])
            if region:
                RegionInfo.update(photo=item['region_photo']).where(RegionInfo.region==region).execute()

        ##uncomment to add region/area to the db

        # if 'region_name' in item.keys():
        #     region = Region.get_or_none(name=item['region_name'])
        #     if not region:
        #         region = Region.create(name=item['region_name'])
        #     region_info = RegionInfo.get_or_none(region=region)
        #     if not region_info:
        #         true_item = {}
        #         for key in item.keys():
        #             true_item[key] = ''
        #             for elem in item[key]:
        #                 if elem!='':
        #                     true_item[key] += elem
        #         RegionInfo.create(region=region, **true_item)
        # if 'area_name' in item.keys():
        #     area = Area.get_or_none(name=item['area_name'])
        #     if not area:
        #         area = Area.create(name=item['area_name'])
        #     if area:
        #         region = Region.get_or_none(name=item['r_name'])
        #         if region:
        #             area.modify_region(region)
        #         area_info = AreaInfo.get_or_none(area=area)
        #         if not area_info:
        #             eye=''
        #             mouth=''
        #             nose=''
        #             food=''
        #             if 'detail' in item.keys():
        #                 for i,detail in enumerate(item['detail']):
        #                     if detail == 'Oeil:':
        #                         eye = item['detail'][i+1]
        #                     if detail == 'Nez:':
        #                         nose = item['detail'][i+1]
        #                     if detail == 'Bouche:':
        #                         mouth = item['detail'][i+1]
        #                     if detail == 'Mets vins:':
        #                         food = item['detail'][i+1]                        
        #             true_kp = ''
        #             if 'keep_advise' in item.keys():
        #                 for kp in item['keep_advise']:
        #                     if kp!='':
        #                         true_kp += kp
        #             true_desc = ''
        #             if 'description' in item.keys():
        #                 for desc in item['description']:
        #                     if desc!='':
        #                         true_desc += desc
        #             photo = ''
        #             if 'photo' in item.keys():
        #                 photo = item['photo']
        #             AreaInfo.create(area=area, eye=eye, nose=nose, mouth=mouth, food=food, description=true_desc, keep_advise=true_kp, photo=photo)
        #         if 'main_grapes' in item.keys():
        #             for grape_name in item['main_grapes']:
        #                 grape = Grape.get_or_none(name=grape_name.upper())
        #                 if grape:
        #                     area_grape = AreaGrape.get_or_none(grape=grape, area=area)
        #                     if not area_grape:
        #                         AreaGrape.create(grape=grape, area=area)
            
class GrapesPipeline(object):
    def process_item(self, item, spider):
        print(item)
        grape = Grape.get_or_none(name=item['name'])
        if not grape:
            true_item = {
                'color':'',
                'name':'',
                'description':''
            }
            for key in item.keys():
                if key == 'description':
                    for desc in item[key]:
                        true_item[key] += desc
                else:
                    true_item[key] = item[key]
            grape = Grape.create(**true_item)
            if 'similar' in item.keys():
                for similar in item['similar']:
                    grape_bis = Grape.get_or_none(name=similar)
                    if grape_bis:
                        grape_synonym = GrapeSynonym.get_or_none(grape_1=grape, grape_2=grape_bis)
                        if not grape_synonym:
                            GrapeSynonym.create(grape_1=grape, grape_2=grape_bis)

class VintagePipeline(object):
    def process_item(self, item, spider):
        area = Area.get_or_none(name=item['area_name'])
        if 'color' in item.keys():
            area_vintage = AreaVintage.get_or_none(area=area, color=item['color'])
            if not area_vintage:
                area_vintage = AreaVintage.create(area=area, color=item['color'], vintage='')
            years = item['years']
            for year in years:
                year_list=year.split(',')
                for single_year in year_list:
                    if single_year != '':
                        area_vintage.add_rank(single_year, item['rank'])
        else:
            area_vintage = AreaVintage.get_or_none(area=area, color='no color')
            if not area_vintage:
                area_vintage = AreaVintage.create(area=area, color='no color', vintage='')
            years = item['years']
            for year in years:
                year_list=year.split(',')
                for single_year in year_list:
                    if single_year != '':
                        area_vintage.add_rank(single_year, item['rank'])