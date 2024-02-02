from flask import Blueprint, jsonify, abort, request
from ..models import Profile, User, Game, Run, liked_games_table, liked_runs_table, db
import sqlalchemy

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('',methods=['POST'])
def create():
    #req body must contain name and profile id
    if 'name' not in request.json:
        return abort(400, description='Request must contain name')
    if 'profile_id' not in request.json:
        return abort(400, description='Request must contain profile_id')
    #profile must exist
    p = Profile.query.get_or_404(request.json['profile_id'], "Profile not found")
    #profile must not be in use
    if db.session.query(User).filter_by(profile_id=request.json['profile_id']).first():
        return abort(400, description='profile already in use')
    #construct user
    u = User(name=request.json['name'],profile_id=request.json['profile_id'])
    db.session.add(u)
    db.session.commit()
    return jsonify(u.serialize())

@bp.route('/<int:id>',methods=['GET'])
def show(id: int):
    #check if user exists
    u = User.query.get_or_404(id, "user not found")
    #return jsonified user
    return jsonify(u.serialize())

@bp.route('/<int:id>',methods=['PATCH','PUT'])
def update(id: int):
    #check if user exists
    u = User.query.get_or_404(id, "user not found")
    #req body must contain name
    if 'name' not in request.json:
        return abort(400, description='Request must contain name')
    #set name to new name
    u.name = request.json['name']
    try:#try to commit the change
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)

@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    #check if user exists
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

@bp.route('/<int:id>/likes', methods = ['POST'])#json will accept game_id or run_id, not both
def likes(id: int):
    User.query.get_or_404(id, "User not found")
    #game_id or run_id must be in json
    if 'game_id' not in request.json and 'run_id' not in request.json:
        return abort(400, description="game_id or run_id is required")
    if 'game_id' in request.json and 'run_id' in request.json:
        return abort(400, description="only accepts game_id OR run_id")
    #handle game liking
    if 'game_id' in request.json:
        Game.query.get_or_404(request.json['game_id'], "Game not found")
        try:
            stmt = sqlalchemy.insert(liked_games_table).values(
            user_id=id, game_id=request.json['game_id'])
            db.session.execute(stmt)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
    #handle run liking
    if 'run_id' in request.json:
        Run.query.get_or_404(request.json['run_id'], "Run not found")
        try:
            stmt = sqlalchemy.insert(liked_runs_table).values(
            user_id=id, run_id=request.json['run_id'])
            db.session.execute(stmt)
            db.session.commit()
            return jsonify(True)
        except:
            return jsonify(False)
