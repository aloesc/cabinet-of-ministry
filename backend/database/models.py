from sqlalchemy import BigInteger, Column, String, LargeBinary, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(String(50), nullable=True)

class Events(Base):
    __tablename__ = "events"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255))
    description = Column(String(1024))
    date_of_event = Column(String(50))
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

    bill_id = Column(BigInteger, ForeignKey("bills.id"), nullable=True)
    first_listening_id = Column(BigInteger, ForeignKey("bills.id"), nullable=True)

class Bills(Base):
    __tablename__ = "bills"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    date_of_uploaded = Column(String(50), nullable=True)
    subject = Column(String(100), nullable=True)
    main_committee = Column(String(100), nullable=True)

    # Один документ как link
    project_bill_id = Column(BigInteger, ForeignKey("documents.id"), nullable=True)
    project_bill = relationship("Documents", uselist=False, foreign_keys=[project_bill_id])


    bills_items = relationship(
        "Documents",
        backref="bill_parent",
        cascade="all, delete-orphan",
        primaryjoin="Documents.bill_id==Bills.id"
    )

    first_listening_items = relationship(
        "Documents",
        backref="first_listening_parent",
        cascade="all, delete-orphan",
        primaryjoin="Documents.first_listening_id==Bills.id"
    )