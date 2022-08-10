#from crypt import methods
from flask import Flask, render_template, request, url_for, redirect, session
#import bcrypt
import pymongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongologinexample'
app.config['MONGO_URL'] = 'mongodb://localhost:27017'

mongo = pymongo.MongoClient('mongodb://localhost:27017')
db=mongo['db']


@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as' + session['username']
    
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users= db.users
    login_user = users.find_one({'name': request.form['username']})
    if login_user:
        #if bcrypt.hashpw(request.form['pass'].encode('utf-8'),login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
        if request.form['pass'] == login_user['password']:

            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users= db.users
        existing_user = users.find_one({'name': request.form['username'] })

        if existing_user is None:
           # hashpass = bcrypt.hashpw(request.form['pass'], encode('utf-8'), bcrypt.gensalt())
           #request.form['pass']
            users.insert_one({'name': request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That user already exists!'
    
    return render_template('registration.html')


if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(debug=True)