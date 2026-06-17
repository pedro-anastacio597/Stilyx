from sqlalchemy.orm import sessionmaker
from models import db

def sessao():
    try:
        session= sessionmaker(bind=db)
        Session= session()
        yield Session
    finally:
        Session.close()