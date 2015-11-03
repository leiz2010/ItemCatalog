from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import ItemType, Base, MenuItem

engine = create_engine('sqlite:///menuwithuser.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
type1 = ItemType(category="Appetizer")
type2 = ItemType(category="Entree")
type3 = ItemType(category="Dessert")
type4 = ItemType(category="Beverage")
session.add(type1)
session.add(type2)
session.add(type3)
session.add(type4)
#session.commit()
item = MenuItem(name="Beef Teriyaki", description="Beef wiht rice.", price="8.99", category="Entree")
session.commit()

print "added menu items!"
