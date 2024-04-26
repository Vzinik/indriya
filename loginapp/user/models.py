from flask import Flask, jsonify,request,redirect,session
from passlib.hash import pbkdf2_sha256
from app import db
import uuid
class User:

    #user session
    def start_session(self,user):
        del user['password']
        session['logged_in']=True
        session['user']=user
        return jsonify({"logged_in":"success"}),200
        


    def signup(self):
        print(request.form)

        #create user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "password": request.form.get('password'),
            "deviceID": request.form.get('deviceID'),

        }

        #Encrypting password before sending it to db
        user['password']=pbkdf2_sha256.encrypt(user['password'])

        #check if entered email already exists
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error": "Email address is already in user"}),400
        
        #insert data to mongodb
        if db.users.insert_one(user):
            print(user)
            return self.start_session(user)

        return jsonify({"error": "Signup Failed"}),400
    
        #signout
    def signout(self):
        session.clear()
        return redirect('/')
    
        #check the login creds
    def login(self):
        user=db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({"error": "invalid login credentials"}),400
    
        #get the air quiality from db of the users device
    def getdata(self):
        data = list(db.data.find({'deviceID': '1234'}))
        for record in data:
            record['_id'] = str(record['_id'])
        return jsonify(data)

class Indriya:

        #gets air quality data from indriya and write it to mongodb
    def submit(self):
        data = {
            "_id": uuid.uuid4().hex,
            "Device Id" : request.form.get('id'),
            "Time Stamp" : request.form.get('time'),
            "Gas Resistance": request.form.get('gas'),
            "Temperature": request.form.get('temp'),
            "Pressure": request.form.get('press'),
            "Relative Humidity": request.form.get('humidity'),
            "GPS": request.form.get('GPS'),
            "IAQ" :request.form.get('iaq'),
            "CO2 equivalent" : request.form.get('CO2'),
            "breath VOC" : request.form.get('bvoc'),
        }
        if db.data.insert_one(data):
            return jsonify({"status":"recieved"}),400
        
        return jsonify({"status":"failed"}),200
        