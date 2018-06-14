import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Guest(Base):
    __tablename__ = 'guest'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    image = Column(String(250))

class Flowershop(Base):
    __tablename__ = 'flowershop'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    guest_id = Column(Integer, ForeignKey('guest.id'))
    guest = relationship(Guest)
    
    @property
    def serialize(self):
        """formart"""
        return {
            'name': self.name,
            'id': self.id,
        }


class AvailableItem(Base):
    __tablename__ = 'available_item'

    nameofflower = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    information = Column(String(250))
    course = Column(String(250))
    price = Column(String(8))
    flowershop_id = Column(Integer, ForeignKey('flowershop.id'))
    flowershop = relationship(Flowershop)
    guest_id = Column(Integer, ForeignKey('guest.id'))
    guest = relationship(Guest)
    @property
    def serialize(self):
        """ serialize format"""
        return {
            'nameofflower': self.nameofflower,
            'information': self.information,
            'id': self.id,
            'course': self.course,
            'price': self.price,
        }


engine = create_engine('sqlite:///flowershop.db')


Base.metadata.create_all(engine)
