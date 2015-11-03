from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, ItemType, MenuItem
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///menu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Revoke the user's token and reset login session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# XML for the entire menu
@app.route('/menu/XML')
def menuXML():
    items = session.query(MenuItem).all()
    return render_template('menu.xml', items=items)

# Json for the entire menu
@app.route('/menu/JSON/')
def menuJSON():
    items = session.query(MenuItem).all()
    return jsonify(MenuItems=[i.serialize for i in items])

# Json endpoint for individual item
@app.route('/menu/<int:item_id>/JSON/')
def menuItemJSON(item_id):
    menuItem = session.query(MenuItem).filter_by(id=item_id).one()
    return jsonify(MenuItem=menuItem.serialize)

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
    #  Prompt the user to login
    if 'username' not in login_session:
        return redirect('/login')
    # Add new menu item to this category type
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            category=category)
        session.add(newItem)
        session.commit()
        flash("New menu item created")
        return redirect(url_for('menu'))
    else:
        return render_template('newitem.html', category=category)


@app.route('/menu/<string:category>/<int:item_id>/edit/',
        methods=['GET', 'POST'])
def editMenuItem(category, item_id):
    #  Prompt the user to login
    if 'username' not in login_session:
        return redirect('/login')
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
    #  Prompt the user to login
    if 'username' not in login_session:
        return redirect('/login')
    # Delete this menu item in this category type
    deleteItem = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        print "Entered POST condition"
        session.delete(deleteItem)
        session.commit()
        flash("Menu item deleted")
        return redirect(url_for('menu'))
    else:
        return render_template('deleteitem.html', item=deleteItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
