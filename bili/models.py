#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import CHAR,Integer,SmallInteger,DateTime,Date,Time
from sqlalchemy import create_engine,Column,PrimaryKeyConstraint,Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert

Base = declarative_base()

class IndexGlobalModel(Base):
    __tablename__ = 'index_global'
    __table_args__ = (
        Index('ix_pub_time','pub_time'),
        Index('ix_update_time','update_time'),
    )
    pub_time = Column(Date)
    update_time = Column(DateTime)
    season_id = Column(Integer,primary_key=True)
    title = Column(CHAR(100))
    badge =Column(CHAR(4))
    is_finish = Column(SmallInteger)
    week = Column(CHAR(2))
    favorites = Column(Integer)
    total_count = Column(SmallInteger)
    url = Column(CHAR(40))
    cover = Column(CHAR(76))
    newest_ep_index = Column(CHAR(40))
    pub_string = Column(CHAR(20))
    season_status = Column(CHAR(2))
    update_pattern = Column(CHAR(20))

class ScoresModel(Base):
    __tablename__ = 'scores'
    __table_args__ = (
        # PrimaryKeyConstraint('aid','pts'),
        Index('dx_scores_dt','dt'),
        Index('dx_scores_aid','aid'),
    )
    id = Column(Integer,primary_key=True, autoincrement=True)
    dt = Column(DateTime)
    aid = Column(Integer)
    pts = Column(Integer)
    coins = Column(Integer)
    play = Column(Integer)
    video_review = Column(Integer)
    bangdan = Column(CHAR(2))
    pinlv = Column(CHAR(2))
    jiange = Column(CHAR(2))
    fenqv = Column(CHAR(2))
    title = Column(CHAR(80))
    author = Column(CHAR(20))
    mid = Column(CHAR(10))
    duration = Column(Time)
    pic = Column(CHAR(76))
    trend = Column(CHAR(10))

class VideoModel(Base):
    __tablename__ = 'video'
    __table_args__ = (
        PrimaryKeyConstraint('aid','pts'),
        Index('dx_video_dt','dt'),
    )
    dt = Column(DateTime)
    aid = Column(Integer)
    view = Column(Integer)
    danmaku = Column(Integer)
    reply = Column(Integer)
    favorite = Column(Integer)
    coin = Column(Integer)
    share = Column(Integer)
    pts = Column(Integer)
    now_rank = Column(Integer)
    his_rank = Column(Integer)
    no_reprint = Column(SmallInteger)
    copyright = Column(SmallInteger)

engine = create_engine(
    get_project_settings().get('MYSQL_URL'),
    # echo=True
)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

@compiles(Insert)
def insert_ignore(insert, compiler, **kw):
    s = compiler.visit_insert(insert, **kw)
    s = s.replace("INSERT INTO", "INSERT IGNORE INTO")
    return s