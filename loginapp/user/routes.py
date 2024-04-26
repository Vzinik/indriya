from flask import Flask
from app import app
from user.models import User,Indriya

#sign up
@app.route('/user/signup/', methods=['POST'])   
def signup():
    return User().signup()

#signout
@app.route('/user/signout/')                        
def signout():
    return User().signout()

 #login
@app.route('/user/login/',methods=['POST'])        
def login():
    return User().login()

#storing data from indriya
@app.route('/indriya/submit/',methods=['POST'])     
def submit():
    return Indriya().submit()

#requesting data from the database
@app.route('/user/data/',methods=['GET'])           
def getdata():
    return User().getdata()
    