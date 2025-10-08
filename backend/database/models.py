from sqlalchemy import BigInteger, Column, String, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(255))
    username = Column(String(150), unique=True)
    password = Column(String(255))
    email = Column(String(255), unique=True)
    phonenumber = Column(String(50))
    date_of_birth = Column(String(50))
    gender = Column(String(20))
    role = Column(String(50), nullable=False, default="guest")
    is_superuser = Column(Boolean, default=False)

class Events(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    description = Column(String(1024))
    date = Column(String(50))
    location = Column(String(255))
    type_of_event = Column(String(100))

class Documents(Base):
    __tablename__ = "documents"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    date_of_uploaded = Column(String(50), nullable=True)
    type_of_document = Column(String(100), nullable=True)
    binary_data = Column(LargeBinary, nullable=True)