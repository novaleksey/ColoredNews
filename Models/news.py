from sqlalchemy import Column, Integer, DateTime, Text

from .base import BaseModel, DBSession


class News(BaseModel):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    subject = Column(Text)
    created_at = Column(DateTime)
    published_at = Column(DateTime)
    category_id = Column(Integer)
    image_id = Column(Integer)
    source_id = Column(Integer)

    def __init__(self, title, url, subject):
        self.title = title
        self.url = url
        self.subject = subject


def create_news(title, url, img_url, source):
    session = DBSession()
    news = News(title, url)
