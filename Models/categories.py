from sqlalchemy import Column, Integer, String, ForeignKey

from .base import BaseModel


class Categories(BaseModel):
    __tablename__ = 'categories'

    id = Column(Integer, ForeignKey('news.category_id'), primary_key=True)
    category_name = Column(String)

    def __init__(self, category_name):
        self.category_name = category_name
