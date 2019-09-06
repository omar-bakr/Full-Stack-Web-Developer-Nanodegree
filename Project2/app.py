import requests
import json
import string
import random
import httplib2
from flask import session as login_session
from flask import flash, make_response
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from database_setup import Category, Item, Base, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
app = Flask(__name__)


# Connect to Database and create database session
engine = create_engine('postgresql+pg8000://catalog:catalog@localhost/catalog')
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


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = '''https://graph.facebook.com/oauth/access_token?grant_type=
    fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s''' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = '''https://graph.facebook.com/v2.8/me?access_token=%s
    &fields=name,id,email''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = '''https://graph.facebook.com/v2.8/me/picture?
    access_token=%s&redirect=0&height=200&width=200''' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
     150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    access_token = login_session.get('access_token')
    facebook_id = login_session['facebook_id']
    if access_token is None:
        login_session.clear()
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session.clear()
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[0]
    if result['status'] != '200':
        login_session.clear()
        return redirect(render_template('index.html'))
    return render_template('logged_out.html')


# Routes
@app.route('/')
@app.route('/catalog')
def home():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    logged_in = is_logged_in()
    return render_template('index.html',
                           categories=categories,
                           items=items,
                           logged_in=logged_in,
                           section_title="Latest Items",
                           )


@app.route('/catalog/<string:category_name>')
def categoryItems(category_name):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_name=category_name).all()
    logged_in = is_logged_in()
    return render_template('index.html',
                           categories=categories,
                           current_category=category_name,
                           items=items,
                           logged_in=logged_in,
                           section_title="%s Items (%d items)" % (
                               category_name, len(items)),
                           )


@app.route('/catalog/<string:category_name>/<string:item_name>')
def OneItem(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    logged_in = is_logged_in()
    user_id = login_session.get('user_id')
    return render_template('item_view.html',
                           item=item,
                           user_id=user_id,
                           logged_in=logged_in,
                           )


@app.route('/catalog/new-item', methods=['GET', 'POST'])
def addNewItem():
    logged_in = is_logged_in()

    if request.method == 'POST':
        user_id = login_session.get('user_id')

        if user_id is None:
            # ensure only authenticated users are allowed
            return render_template('error.html',
                                   error='Invalid user',
                                   logged_in=logged_in)

        category = request.form['category_name']
        item_name = request.form['name']
        item_description = request.form['description']

        if category is None or category.strip() == '':
            return render_template('error.html',
                                   error='Invalid category name',
                                   logged_in=logged_in)

        if item_name is None or item_name.strip() == '':
            return render_template('error.html',
                                   error='Invalid item name',
                                   logged_in=logged_in)

        item = Item(name=item_name,
                    description=item_description,
                    user_id=user_id,
                    category_name=category)
        session.add(item)
        session.commit()
        flash('New item added')
        return redirect(url_for('OneItem',
                                category_name=item.category_name,
                                item_name=item.name))
    else:
        categories = session.query(Category).all()
        return render_template('item_add.html',
                               categories=categories,
                               logged_in=logged_in)


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    logged_in = is_logged_in()
    item = session.query(Item).filter_by(name=item_name).one()
    user_id = login_session.get('user_id')

    if request.method == 'POST':

        if user_id is None or user_id != item.user_id:
            # ensure only authorized users are allowed
            return render_template('error.html',
                                   error='Invalid user',
                                   logged_in=logged_in)

        category = request.form['category_name']
        new_name = request.form['name']
        new_description = request.form['description']

        if category is None or category.strip() == '':
            return render_template('error.html',
                                   error='Invalid category name',
                                   logged_in=logged_in)

        if new_name is None or new_name.strip() == '':
            return render_template('error.html',
                                   error='Invalid item name',
                                   logged_in=logged_in)

        item.name = new_name
        item.description = new_description
        item.category_name = category

        session.add(item)
        session.commit()
        flash('Item edited')
        return redirect(url_for('OneItem',
                                category_name=item.category_name,
                                item_name=item.name))
    else:
        categories = session.query(Category).all()
        return render_template('item_edit.html',
                               categories=categories,
                               item=item,
                               user_id=user_id,
                               logged_in=logged_in)


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    logged_in = is_logged_in()
    item = session.query(Item).filter_by(name=item_name).one()
    user_id = login_session.get('user_id')

    if request.method == 'POST':

        if user_id is None or user_id != item.user_id:
            # ensure only authorized users are allowed
            return render_template('error.html',
                                   error='Invalid user',
                                   logged_in=logged_in)

        session.delete(item)
        session.commit()

        flash('Item deleted')
        return redirect(url_for('home'))
    else:
        return render_template('item_delete.html',
                               item=item,
                               user_id=user_id,
                               logged_in=logged_in)


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# JSON end-points
@app.route('/catalog.json')
def catalogjson():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return jsonify(
        categories=[
            c.serialize for c in categories], Items=[
            i.serialize for i in items])


@app.route('/catalog/<string:category_name>.json')
def categoryItemsjson(category_name):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_name=category_name).all()
    return jsonify(
        categories=[
            c.serialize for c in categories], Items=[
            i.serialize for i in items])


@app.route('/catalog/<string:category_name>/<string:item_name>.json')
def OneItemjson(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    return jsonify(Items=[i.serialize for i in items])

# user helper functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


def is_logged_in():
    return login_session.get('access_token') is not None


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
