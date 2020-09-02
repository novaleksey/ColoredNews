from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# TODO Получать конфиги из переменных окружения
user, password, host, port, db_name = 'postgres', 'postgres', 'localhost', '5432', 'News'

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')
DBSession = sessionmaker(bind=engine)

BaseModel = declarative_base()
