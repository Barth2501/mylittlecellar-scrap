from peewee import *
from playhouse.postgres_ext import ArrayField
from playhouse.migrate import *

from .base_model import BaseModel
from .area import Area

from scrapping.cellar_scrapy.database import db


migrator = PostgresqlMigrator(db)

class Category(BaseModel):
    id = AutoField()
    name = CharField()

class Recipe(BaseModel):
    id = AutoField()
    name = TextField()
    ingredients = ArrayField(TextField, null=True)
    preparation = ArrayField(TextField, null=True)
    image = TextField(null=True)
    category = ForeignKeyField(Category, backref='recipes')
    proportion=CharField(null=True)
    time_prep=CharField(null=True)
    time_cook=CharField(null=True)
    description=TextField(null=True)

    def get_data(self):
        data = self.get_small_data()
        data['wines'] = [w.get_small_data() for w in self.wines]
        return data

    def modify_ing(self):
        return Recipe.update(ingredients=[self.name]).where(Recipe.id==self.id).execute()

class AreaRecipe(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='recipes')
    recipe = ForeignKeyField(Recipe, backref='areas')

with db:
    Recipe.create_table(safe=True)