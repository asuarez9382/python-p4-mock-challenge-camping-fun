#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    
    def get(self):
        
        campers = Camper.query.all()
        
        campers_dict = [ camper.to_dict( only=('id','name','age')) for camper in campers ]
        
        response = make_response(
            campers_dict,
            200
        )
        
        return response 
    
    def post(self):
        
        data = request.get_json()
    
        
        try:
            
            camper = Camper(
                name=data['name'],
                age=data['age']
            )
            
            db.session.add(camper)
            db.session.commit()
            
            camper_dict = camper.to_dict()
            
            response = make_response(
                jsonify(camper_dict),
                201
            )
            
            return response 
        except:
            return { "errors": ["validation errors"] }, 400
    
class CampersByID(Resource):
    
    def get(self, id):
        
        camper = Camper.query.filter_by(id = id).first()
        
        if not camper:
            return { 'error': 'Camper not found' }, 404
            
        camper_dict = camper.to_dict()
        
        response = make_response(
            camper_dict,
            200
        )
        
        return response 
    
    def patch(self, id):
        
        data = request.get_json()
        
        try:
            camper = Camper.query.filter_by(id=id).first()
            
            camper.name = data['name']
            camper.age = data['age']
            
            db.session.commit()
            
            camper_dict = camper.to_dict()
            
            response = make_response(
                camper_dict,
                202
            )
            
            return response 
        
        except:
            return { "error": "Camper not found" }, 404
        
class Activities(Resource):
    
    def get(self):
        
        activities = Activity.query.all()
        
        activities_dict = [ activity.to_dict(only=("id","name","difficulty")) for activity in activities ]
        
        response = make_response(
            activities_dict,
            200
        )
        
        return response 
    
class ActivitiesByID(Resource):
    
    def get(self, id):
        
        activity = Activity.query.filter_by(id = id).first()
        
        if not activity:
            return {"error": "Activity not found"}, 404
        
        activity_dict = activity.to_dict()
        
        response = make_response(
            activity_dict,
            200
        )
        
        return response 
    
    def delete(self, id):
        
        activity = Activity.query.filter_by(id = id).first()
        
        if not activity:
            return {"error": "Activity not found"}, 404
        
        db.session.delete(activity)
        db.session.commit()
        
        return {}, 204
        
class Signups(Resource):
    
    def get(self):
        
        signups = Signup.query.all()
        
        signups_dict = [ signup.to_dict() for signup in signups ]
        
        response = make_response(
            signups_dict,
            200
        )
        
        return response
    
    def post(self):
        
        data = request.get_json()
        
        try:
            
            signup = Signup(
                camper_id= data['camper_id'],
                activity_id= data['activity_id'],
                time= data['time']
            )
            
            db.session.add(signup)
            db.session.commit()
            
            signup_dict = signup.to_dict()
            
            response = make_response(
                signup_dict,
                201
            )
            
            return response 
    
        except:
            return { "errors": ["validation errors"] }, 400
        
api.add_resource(Campers, "/campers")
api.add_resource(CampersByID, "/campers/<int:id>")
api.add_resource(Activities, "/activities")
api.add_resource(ActivitiesByID, "/activities/<int:id>")
api.add_resource(Signups, "/signups")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
