from flask import Flask, jsonify, url_for, flash
from flask import render_template, request, redirect
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Flowershop, Base, AvailableItem, Guest

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('secret_client.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Flowershop Menu Application"

# It will connect to the database and it will create sessions
engine = create_engine('sqlite:///flowershop.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:

        oauth_flow = flow_from_clientsecrets('secret_client.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    resultt = ''
    resultt += '<h2>Welcome Mr/Mrs, '
    resultt += login_session['username']
    resultt += '!</h2>'
    resultt += '<img src="'
    resultt += login_session['picture']
    resultt += ' " style = "width: 350px;'
    resultt += 'height: 350px;'
    resultt += 'border-radius: 140px;'
    resultt += '-webkit-border-radius: 150px;'
    resultt += '-moz-border-radius: 150px;"> '
    flash("you logged in as %s" % login_session['username'])
    print "Sucessfully Done!!"
    return resultt


def createGuest(login_session):
    newGuest = User(
        username=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'])
    session.add(newGuest)
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
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('User Not Connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Disconnected Sucessfully.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('rovoke token dailed for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/flowershop/<int:flowershop_id>/product/JSON')
def flowershopproductJSON(flowershop_id):
    flowershop = session.query(Flowershop).filter_by(id=flowershop_id).one()
    products = session.query(AvailableItem).filter_by(
        flowershop_id=flowershop_id).all()
    return jsonify(AvailableItem=[i.serialize for i in products])


@app.route('/flowershop/<int:flowershop_id>/product/<int:product_id>/JSON')
def flowerMenuJSON(flowershop_id, product_id):
    Menu_Items = session.query(AvailableItem).filter_by(id=product_id).one()
    return jsonify(Menu_Items=Menu_Items.serialize)


@app.route('/flowershop/JSON')
def flowershopsJSON():
    flowershops = session.query(Flowershop).all()
    return jsonify(flowershops=[r.serialize for r in flowershops])

# Display Flowershops


@app.route('/')
@app.route('/flowershop/')
def showflowerShops():
    sess1 = DBSession()
    flowershops = sess1.query(Flowershop).order_by(asc(Flowershop.name))
    sess1.close()
    return render_template('Flowershops.html', flowershops=flowershops)

# Create New Flowershop


@app.route('/flowershop/new/', methods=['GET', 'POST'])
def newFlowershop():
    sess2 = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newFlowershop = Flowershop(name=request.form['name'])
        sess2.add(newFlowershop)
        flash('New Flowershop %s Successfully Created' % newFlowershop.name)
        sess2.commit()
        sess2.close()
        return redirect(url_for('showflowerShops'))
    else:
        return render_template('NewFlowershop.html')

# Edit FlowerShop


@app.route('/flowershop/<int:flowershop_id>/edit/', methods=['GET', 'POST'])
def editFlowershop(flowershop_id):
    sess3 = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editedFlowershop = sess3.query(Flowershop).filter_by(
        id=flowershop_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedFlowershop.name = request.form['name']
            sess3.add(editedFlowershop)
            sess3.commit()
            flash('Flowershop Edited %s' % editedFlowershop.name)
            sess3.close()
            return redirect(url_for('showflowerShops'))
    else:
        return render_template(
            'EditFlowershop.html', flowershop=editedFlowershop)


# Show Flowers in the Shop
@app.route('/flowershop/<int:flowershop_id>/')
@app.route('/flowershop/<int:flowershop_id>/product/')
def showProduct(flowershop_id):
    sess5 = DBSession()
    flowershop = sess5.query(Flowershop).filter_by(id=flowershop_id).one()
    products = sess5.query(AvailableItem).filter_by(
        flowershop_id=flowershop_id).all()
    sess5.close()
    return render_template(
        'AvailableItem.html', products=products, flowershop=flowershop)

# Create New Items In Shop


@app.route(
    '/flowershop/<int:flowershop_id>/product/new/', methods=['GET', 'POST'])
def newProducts(flowershop_id):
    sess6 = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    flowershop = sess6.query(Flowershop).filter_by(id=flowershop_id).one()
    if request.method == 'POST':
        newItem = AvailableItem(
            nameofflower=request.form['name'],
            price=request.form['price'],
            course=request.form['course'],
            flowershop_id=flowershop_id,
            guest_id=flowershop.guest_id)
        sess6.add(newItem)
        sess6.commit()
        flash('New Flower %s Created' % (newItem.nameofflower))
        sess6.close()
        return redirect(url_for('showProduct', flowershop_id=flowershop_id))
    else:
        return render_template('NewItem.html', flowershop_id=flowershop_id)

# Edit Flower name and price and course


@app.route(
    '/flowershop/<int:flowershop_id>/product/<int:product_id>/edit',
    methods=['GET', 'POST'])
def editProducts(flowershop_id, product_id):
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    editedFlower = session.query(AvailableItem).filter_by(id=product_id).one()
    flowershop = session.query(Flowershop).filter_by(id=flowershop_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedFlower.nameofflower = request.form['name']
        if request.form['price']:
            editedFlower.price = request.form['price']
        if request.form['course']:
            editedFlower.course = request.form['course']
        session.add(editedFlower)
        session.commit()
        session.close()
        flash('Flower Edited')
        return redirect(url_for('showProduct', flowershop_id=flowershop_id))
    else:
        return render_template(
            'EditItem.html',
            flowershop_id=flowershop_id,
            product_id=product_id,
            product=editedFlower)

# Delete Flowers


@app.route(
    '/flowershop/<int:flowershop_id>/product/<int:product_id>/delete',
    methods=['GET', 'POST'])
def deleteItems(flowershop_id, product_id):
    if 'username' not in login_session:
        return redirect('/login')
    flowershop = session.query(Flowershop).filter_by(id=flowershop_id).one()
    FlowerToDelete = session.query(AvailableItem).filter_by(
        id=product_id).one()
    if request.method == 'POST':
        session.delete(FlowerToDelete)
        session.commit()
        flash('Flower Delete Success')
        return redirect(url_for('showProduct', flowershop_id=flowershop_id))
    else:
        return render_template('DeleteItem.html', product=FlowerToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
