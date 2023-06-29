from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://your_username:your_password@your_host:your_port/your_database')
Session = sessionmaker(bind=engine)