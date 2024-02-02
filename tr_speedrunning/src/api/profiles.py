from flask import Blueprint, jsonify, abort, request
from ..models import Profile, User, db
import sqlalchemy

bp = Blueprint('profiles', __name__, url_prefix='/profiles')

@bp.route('',methods=['POST'])
def create():
    #req body must contain email address and address
    if 'email' not in request.json:
        return abort(400, description='Request must contain email')
    if 'address' not in request.json:
        return abort(400, description='Request must contain address')
    #email address must be unique
    if db.session.query(Profile).filter_by(email=request.json['email']).first():
        return abort(400, description='Email already in use')
    #construct profile
    p = Profile(email=request.json['email'],address=request.json['address'])
    db.session.add(p)
    db.session.commit()
    return jsonify(p.serialize())

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    #check if profile exists
    p = Profile.query.get_or_404(id, "Profile not found")
    #return jsonified profile
    return jsonify(p.serialize())

@bp.route('/<int:id>',methods=['PATCH','PUT'])
def update(id: int):
    #check if profile exists
    p = Profile.query.get_or_404(id, "profile not found")
    #req body must contain email or address
    if 'email' not in request.json and 'address' not in request.json:
        return abort(400, description='Request must contain email or address')
    #set value/s to new value/s
    if 'email' in request.json:
        #email address must be unique
        if db.session.query(Profile).filter_by(email=request.json['email']).first():
            return abort(400, description='Email already in use')
        p.email = request.json['email']
    if 'address' in request.json:
        p.address = request.json['address']
    try:#try to commit the change
        db.session.commit()
        return jsonify(p.serialize())
    except:
        return jsonify(False)

@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    #check if Profile exists
    p = Profile.query.get_or_404(id, "Profile not found")
    try:
        db.session.delete(p) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)