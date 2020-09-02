from sqlalchemy import Column, Integer, String, ForeignKey

from .base import BaseModel


class Sources(BaseModel):
    __tablename__ = 'sources'

    id = Column(Integer, ForeignKey('news.source_id'), primary_key=True)
    url = Column(String)
    brief = Column(String)

    def __init__(self, url, brief):
        self.url = url
        self.brief = brief
