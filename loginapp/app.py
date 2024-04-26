from flask import Flask,render_template,session,redirect
from functools import wraps
import pymongo
import os

#environment variables
MONGO_USERNAME=os.environ['MONGO_USERNAME']
MONGO_PASSWORD=os.environ['MONGO_PASSWORD']
MONGO_PORT=os.environ['MONGO_PORT']
MONGO_DB=os.environ['MONGO_DB']
USER_COLLECTION=os.environ['USER_COLLECTION']
DATA_COLLECTION=os.environ['DATA_COLLECTION']
MONGO_HOST=os.environ['MONGO_HOST']

POSTGRES_PASSWORD=os.environ['POSTGRES_PASSWORD']



app=Flask(__name__)
app.secret_key='random_binary_string.'


#Mongo Database
mongo_uri=f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
client = pymongo.MongoClient(mongo_uri)
db = client.user_login_system
def is_logged_in(f):
    @wraps(f)
    def wrap(*arg,**kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect('/')
    return wrap



#routes
from user import routes


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup/')
def login_form():
    return render_template('signup.html')


if __name__== "__main__":
    app.debug=True
    app.run(host="0.0.0.0", port=5000)