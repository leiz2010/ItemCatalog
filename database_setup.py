import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class ItemType(Base):
    __tablename__ = 'ItemType'

    id = Column(Integer, primary_key=True)
    category = Column(String(80), nullable=False, unique=True)

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class MenuItem(Base):
    __tablename__ = 'MenuItem'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String, ForeignKey('ItemType.category'))
    item_type = relationship(ItemType)
    user_id = Column(Integer, ForeignKey('User.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category': self.category,
            'user_id': self.user_id
        }

engine = create_engine('sqlite:///menuwithuser.db')

Base.metadata.create_all(engine)
