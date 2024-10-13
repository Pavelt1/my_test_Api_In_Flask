import os

import datetime

import sqlalchemy 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER',"postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD',"0596")
POSTGRES_DB = os.getenv('POSTGRES_DB',"postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","5432")

DSN = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_HOST}/{POSTGRES_DB}"
engine = sqlalchemy.create_engine(DSN)

metadata = sqlalchemy.MetaData()
Base = declarative_base(metadata=metadata)


class Users(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String,nullable=False)

    announcement = relationship("Announcement", back_populates="user")

    def dict(self):
        return{
            "id":self.id,
            "username":self.username
            }

class Announcement(Base):
    __tablename__ = "announcement"

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime,nullable=False, default=datetime.datetime.utcnow)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')) 

    user = relationship("Users", back_populates="announcement")

    @property
    def dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "text":self.text,
            "date":self.date,
            "user":self.user_id
            }
    

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Creating database")
