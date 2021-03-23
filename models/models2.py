from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float,DateTime,Boolean,ForeignKey,BigInteger,Text
import configparser
from os import getcwd

engine  = create_engine(f'mysql+pymysql://root:vDJinm23@localhost:3306/teste')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base    = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    addresses = relationship('Address', backref='person', lazy=True)
    cars      = relationship('Car',backref='person',lazy=True)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'),nullable=False)


class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    modelo = Column(String(120), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'),nullable=False)

if not engine.dialect.has_table(engine, 'parent'):
    Base.metadata.create_all(engine)