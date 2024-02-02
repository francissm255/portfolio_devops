from flask import Blueprint, jsonify, abort, request
from ..models import Game, User, Run, db
import sqlalchemy

bp = Blueprint('runs', __name__, url_prefix='/runs')

@bp.route('',methods=['POST'])
def create():
    #req body must contain time, game_id, and user_id
    if 'time' not in request.json:
        return abort(400, description='Request must contain time')
    if 'game_id' not in request.json:
        return abort(400, description='Request must contain game_id')
    if 'user_id' not in request.json:
        return abort(400, description='Request must contain user_id')
    #game must exist
    g = Game.query.get_or_404(request.json['game_id'], "Game not found")
    #user must exist
    u = User.query.get_or_404(request.json['user_id'], "User not found")
    #construct run
    r = Run(time=request.json['time'],game_id=request.json['game_id'],user_id=request.json['user_id'])
    db.session.add(r)
    db.session.commit()
    return jsonify(r.serialize())

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    #check if run exists
    r = Run.query.get_or_404(id, "Run not found")
    #return jsonified run
    return jsonify(r.serialize())

@bp.route('/<int:id>',methods=['PATCH','PUT'])
def update(id: int):
    #check if run exists
    r = Run.query.get_or_404(id, "Run not found")
    #req body must contain name
    if 'time' not in request.json:
        return abort(400, description='Request must contain time')
    #set time to new time
    r.time = request.json['time']
    try:#try to commit the change
        db.session.commit()
        return jsonify(r.serialize())
    except:
        return jsonify(False)

@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    #check if run exists
    r = Run.query.get_or_404(id, "Run not found")
    try:
        db.session.delete(r) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)