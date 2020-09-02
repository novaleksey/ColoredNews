from sqlalchemy import Column, Integer, String

from .base import BaseModel


class Settings(BaseModel):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    setting_key = Column(String)
    setting_value = Column(String)

    def __init__(self, setting_key, setting_value):
        self.setting_key = setting_key
        self.setting_value = setting_value
