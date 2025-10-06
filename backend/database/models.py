from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    phonenumber = Column(String)
    date_of_birth = Column(String)
    gender = Column(String)
    role = Column(String)

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(String)
    location = Column(String)
    type_of_event = Column(String)

class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    description = Column(String)
    date_of_uploaded = Column(String, nullable=True)
    type_of_document = Column(String, nullable=True)
    binary_data = Column(LargeBinary, nullable=True)