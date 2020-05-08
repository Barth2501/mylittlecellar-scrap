from peewee import *
from playhouse.sqlite_ext import *
from playhouse.postgres_ext import ArrayField

from .base_model import BaseModel
from .region import Region
from scrapping.cellar_scrapy.database import db


class Area(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    region = ForeignKeyField(Region, backref='areas', null=True)

    def modify_region(self, region):
        return Area.update(region=region).where(Area.name==self.name).execute()

    def get_info_grapes_data(self):
        data = self.get_small_data()
        data['info'] = AreaInfo.get_or_none(area=self).get_small_data()
        data['grapes'] = [g.grape.get_small_data() for g in self.grapes]
        return data

class AreaInfo(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='info')
    description = TextField(null=True)
    photo = CharField(null=True)
    keep_advise = TextField(null=True)
    eye = TextField(null=True)
    nose = TextField(null=True)
    mouth = TextField(null=True)
    food = TextField(null=True)

class Grape(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    color = CharField(null=True)
    description = TextField(null=True)

class GrapeSynonym(BaseModel):
    id = AutoField()
    grape_1 = ForeignKeyField(Grape, backref='synonym')
    grape_2 = ForeignKeyField(Grape, backref='synonym')

class AreaGrape(BaseModel):
    id = AutoField()
    grape = ForeignKeyField(Grape, backref='areas')
    area = ForeignKeyField(Area, backref='grapes')

class AreaVintage(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='vintage')
    color = CharField()
    vintage = TextField()

    def add_rank(self, year, rank):
        #vintage_list = self.vintage
        #vintage_list = vintage_list +",{'vintage':{},'rank':{}}".format(year,rank)
        data = {year:rank}
        AreaVintage.update({
                AreaVintage.vintage: AreaVintage.vintage.concat(data)
            }).where(AreaVintage.id==self).execute()
        return AreaVintage.update({
                AreaVintage.vintage: AreaVintage.vintage.concat(',')
            }).where(AreaVintage.id==self).execute()

with db:
    AreaVintage.create_table(safe=True)