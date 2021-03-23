from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Float,DateTime,Boolean,ForeignKey,Integer,Text
import configparser
from os import getcwd

engine  = create_engine(f'mysql+pymysql://root:vDJinm23@localhost:3306/webmotors1')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base    = declarative_base()

class Media(Base):
    __tablename__ = "medias"
    id          = Column(Integer,primary_key=True)
    photoPath   = Column(String(256))
    vehicle_id  = Column(Integer,ForeignKey("vehicles.id"),nullable=False)

class Attribute(Base):
    __tablename__ = "attributes"
    id          = Column(Integer,primary_key=True)
    name        = Column(String(512))
    vehicle_id  = Column(Integer,ForeignKey("vehicles.id"),nullable=False)

class Vehicle(Base):
    __tablename__   = "vehicles"
    id              = Column(Integer,primary_key=True)
    typeVehicle     = Column(String(16))
    armored         = Column(Boolean)
    price           = Column(Float)
    listingType     = Column(String(4))
    productCode     = Column(Integer)
    comment         = Column(Text)
    fipePercent     = Column(Float)
    title           = Column(String(512))
    yearFabrication = Column(String(32))
    yearModel       = Column(Float)
    odometer        = Column(Float)
    transmission    = Column(String(16))
    numberPorts     = Column(Integer)
    bodyType        = Column(String(32))
    medias          = relationship(Media,backref='vehicles',lazy=True)
    attributes      = relationship(Attribute,backref="vehicles",lazy=True)
    color_id        = Column(Integer,ForeignKey("colors.id"),nullable=False)
    model_id        = Column(Integer,ForeignKey("models.id"),nullable=False)
    version_id      = Column(Integer,ForeignKey("versions.id"),nullable=True)
    make_id         = Column(Integer,ForeignKey("makes.id"),nullable=False)
    seller_id       = Column(Integer,ForeignKey("sellers.id"),nullable=False)


class Color(Base):
    __tablename__ = "colors"
    id         = Column(Integer,primary_key=True)
    primary    = Column(String(16))
    vehicles   = relationship("Vehicle",backref="color",lazy=True)

class Model(Base):
    __tablename__ = "models"
    id         = Column(Integer,primary_key=True)
    value      = Column(String(256))
    vehicles   = relationship("Vehicle",backref="model",lazy=True)

class Version(Base):
    __tablename__ = "versions"
    id         = Column(Integer,primary_key=True)
    value      = Column(String(256))
    vehicles   = relationship("Vehicle",backref="version",lazy=True)

class Make(Base):
    __tablename__ = "makes"
    id         = Column(Integer,primary_key=True)
    value      = Column(String(256))
    vehicles   = relationship("Vehicle",backref="make",lazy=True)

class Seller(Base):
    __tablename__     = "sellers"
    id                = Column(Integer,primary_key=True)
    sellerType        = Column(String(8))
    city              = Column(String(64))
    state             = Column(String(32))
    budgetInvestiment = Column(Float)
    dealerScore       = Column(Integer)
    carDelivery       = Column(Boolean)
    trocaComTroco     = Column(Boolean)
    exceededPlan      = Column(Boolean)
    vehicle           = relationship("Vehicle",backref='seller',lazy=True)

if not engine.dialect.has_table(engine, 'vehicles'):
    Base.metadata.create_all(engine)    