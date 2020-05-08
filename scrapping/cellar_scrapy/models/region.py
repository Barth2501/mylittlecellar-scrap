from peewee import *
# from playhouse.migrate import *

from scrapping.cellar_scrapy.database import db

from .base_model import BaseModel
# migrator = PostgresqlMigrator(db)

class Region(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

class RegionInfo(BaseModel):
    id = AutoField()
    region = ForeignKeyField(Region, backref='info')
    description = TextField(null=True)
    wine_style = TextField(null=True)
    history = TextField(null=True)
    weather_and_soil = TextField(null=True)
    region_map = CharField(null=True)
    photo = CharField(null=True)

with db:
    # migrate(migrator.add_column('regioninfo','photo',RegionInfo.photo))
    Region.create_table(safe=True)
    RegionInfo.create_table(safe=True)