from flask import flask
app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)

@app.route('/')
@app.route('/restaurants')
def restaurants():
    return "all restaurants pagae"

@app.rout('/restaurant/new')
def newRestaurant():
    return "create a new restaurant"

@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "edit restaurant"

@app.route('restaurant/<int:restaurant_id>/delete')
def deletRestaurant(restaurant_id):
    return "delte restaurant"

@app.route('restaurant/<int:restaurant_id>/menu')
def menu(restaurant_id):
    return "restaurant menu"

@app.route('restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return "add menu item"

@app.route('restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "edit menu item"

@app.route('restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "delete menu item"
