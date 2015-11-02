from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, ItemType, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///menu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/menu/')
def menu():
    # Display all menu items
    categories = session.query(ItemType).all()
    items = session.query(MenuItem).all()
    return render_template('menu.html', categories=categories, items=items);


@app.route('/menu/<string:category>/new/',
        methods=['GET', 'POST'])
def newMenuItem(category):
    # Add new menu item to this category type
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            category=category)
        session.add(newItem)
        session.commit()
        flash("new menu item created")
        return redirect(url_for('menu'))
    else:
        return render_template('newitem.html', category=category)


@app.route('/menu/<string:category>/<int:item_id>/edit/',
        methods=['GET', 'POST'])
def editMenuItem(category, item_id):
    # Edit menu item in this category type
    editedItem = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['category']:
            editedItem.category = request.form['category']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("Menu item edited")
        return redirect(url_for('menu'))
    else:
        return render_template('edititem.html', category=category, item=editedItem)


@app.route('/menu/<string:category>/<int:item_id>/delete/',
        methods=['GET', 'POST'])
def deleteMenuItem(category, item_id):
    # Delete this menu item in this category type
    deleteItem = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        print "Entered POST condition"
        session.delete(deleteItem)
        session.commit()
        #flash("Menu item deleted")
        return redirect(url_for('menu'))
    else:
        return render_template('deleteitem.html', item=deleteItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
