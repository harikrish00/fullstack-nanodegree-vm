from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_bootstrap import Bootstrap
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from forms import RestaurantForm, RestaurantMenuForm

app = Flask(__name__)
bootstrap = Bootstrap(app)

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def restaurant_index():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurant.html',restaurants=restaurants)

@app.route('/restaurant/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/new', methods=['GET','POST'])
def new_restaurant():
    form = RestaurantForm()
    if request.method == 'POST':
        name= request.form['name']
        restaurant = Restaurant(name = name)
        session.add(restaurant)
        session.commit()
        flash('Restaurant has been created successfully!','success')
        return redirect(url_for('restaurant_index'))
    else:
        return render_template('new_restaurant.html',form=form)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def edit_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    form = RestaurantForm()
    form.name.data = restaurant.name
    if request.method == 'POST':
        name = request.form['name']
        restaurant.name = name
        session.add(restaurant)
        session.commit()
        flash('Restaurant has been updated successfully!','success')
        return redirect(url_for('restaurant_index'))
    else:
        return render_template('edit_restaurant.html',restaurant = restaurant, form=form)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant has been deleted successfully!','success')
        return redirect(url_for('restaurant_index'))
    else:
        return render_template('delete_restaurant.html',restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menuitem/new', methods=['GET','POST'])
def new_menu_item(restaurant_id):
    name = None
    description = None
    price = None
    form = RestaurantMenuForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        item = MenuItem(name=name, description=description, price=price, restaurant_id=restaurant_id)
        session.add(item)
        session.commit()
        flash('New menu item has been created','success')
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    return render_template('new_menu_item.html',restaurant_id=restaurant_id,form=form)

@app.route('/restaurant/<int:restaurant_id>/menuitem/<int:menu_id>/edit', methods=['GET','POST'])
def edit_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    form = RestaurantMenuForm(obj=item)
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data
        item.name = name
        item.description = description
        item.price = price
        session.add(item)
        session.commit()
        flash('Menu item has been edited','success')
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
    return render_template('edit_menu_item.html', form=form, item = item, restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menuitem/<int:menu_id>/delete', methods=['GET','POST'])
def delete_menu_item(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu item has been deleted','success')
        return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
    else:
        return render_template('delete_menu_item.html', restaurant_id = restaurant_id, item = item)


if __name__ == '__main__':
    app.secret_key = "Super secret"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
