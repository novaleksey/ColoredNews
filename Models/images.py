from sqlalchemy import Column, Integer, String, ForeignKey

from .base import BaseModel


class Images(BaseModel):
    __tablename__ = 'images'

    id = Column(Integer, ForeignKey('news.image_id'), primary_key=True)
    path = Column(String)

    def __init__(self, path):
        self.path = path