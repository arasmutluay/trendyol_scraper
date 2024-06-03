from sqlalchemy import create_engine, Column, Integer, String, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()



class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    rating = Column(Numeric(3, 1))
    comments_count = Column(Integer)


Base.metadata.create_all(engine)
