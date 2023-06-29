from sqlalchemy import select
from models import Embedding
from database import Session

def create_embeddings_table():
    Embedding.__table__.create(bind=Session().bind, checkfirst=True)

def insert_embedding(embedding, user_id):
    session = Session()
    new_embedding = Embedding(user_id, embedding=embedding)
    session.add(new_embedding)
    session.commit()
    session.close()

def find_most_similar_embedding(embedding):
    session = Session()
    result = session.scalars(
        select(Embedding.user_id).order_by(
            Embedding.embedding.l2_distance(embedding)
        ).limit(1)
    )
    session.close()
    return result[0] if result else None