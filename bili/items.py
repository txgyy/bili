# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from .models import IndexGlobalModel,ScoresModel,VideoModel
from six import with_metaclass
from scrapy.item import Field, Item, ItemMeta

class SqlalchemyItemMeta(ItemMeta):

    def __new__(mcs, class_name, bases, attrs):
        cls = super(SqlalchemyItemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        if cls.sqlalchemy_model:
            cls._model_fields = []
            for model_field in cls.sqlalchemy_model.__table__.columns:
                    if model_field.name not in cls.fields:
                        cls.fields[model_field.name] = Field()
        return cls

class SqlalchemyItem(with_metaclass(SqlalchemyItemMeta, Item)):
    sqlalchemy_model = None


class IndexGlobalItem(SqlalchemyItem):
    sqlalchemy_model = IndexGlobalModel

class ScoresItem(SqlalchemyItem):
    sqlalchemy_model = ScoresModel


class VideoItem(SqlalchemyItem):
    sqlalchemy_model = VideoModel
