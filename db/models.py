from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class Embedding(Base):
    __tablename__ = 'embeddings'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    embedding = mapped_column(Vector)