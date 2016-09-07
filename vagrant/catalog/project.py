from flask import Flask, render_template, url_for, request, redirect, flash
from database_setup import Base, MenuItem, Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menuitem/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        name = request.form['menuitem']
        item = MenuItem(name = name, restaurant_id = restaurant_id)
        session.add(item)
        session.commit()
        flash('New menu item has been created')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('new_menu_item.html',restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/edit', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        name = request.form['menuitem']
        item.name = name
        session.add(item)
        session.commit()
        flash('Menu item has been edited')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        item = session.query(MenuItem).filter_by(id = menu_id, restaurant_id = restaurant_id).one()
        return render_template('edit_menu_item.html', item = item, restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu item has been deleted')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant_id = restaurant_id, item = item)

if __name__ == '__main__':
    app.secret_key = 'super secret'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
