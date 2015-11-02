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


class MenuItem(Base):
    __tablename__ = 'MenuItem'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    category = Column(String, ForeignKey('ItemType.category'))
    item_type = relationship(ItemType)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'category': self.category
        }

engine = create_engine('sqlite:///menu.db')

Base.metadata.create_all(engine)
