import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

user_name = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')
database = os.environ.get('POSTGRES_DB')


engine = create_engine(f'postgresql+psycopg2://{user_name}:{password}@{host}:{port}/{database}')
Session = sessionmaker(bind=engine)