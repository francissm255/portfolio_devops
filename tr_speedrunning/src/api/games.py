from flask import Blueprint, jsonify, abort, request
from ..models import Game, User, db
import sqlalchemy

bp = Blueprint('games', __name__, url_prefix='/games')

@bp.route('',methods=['POST'])
def create():
    #req body must contain name
    if 'name' not in request.json:
        return abort(400, description='Request must contain name')
    #construct game
    g = Game(name=request.json['name'])
    db.session.add(g)
    db.session.commit()
    return jsonify(g.serialize())

@bp.route('/<int:id>',methods=['GET'])
def show(id:int):
    #check if game exists
    g = Game.query.get_or_404(id, "Game not found")
    #return jsonified game
    return jsonify(g.serialize())

@bp.route('/<int:id>',methods=['PATCH','PUT'])
def update(id: int):
    #check if game exists
    g = Game.query.get_or_404(id, "Game not found")
    #req body must contain name
    if 'name' not in request.json:
        return abort(400, description='Request must contain name')
    g.name = request.json['name']#set the name to the new name
    try:#try to commit the change
        db.session.commit()
        return jsonify(g.serialize())
    except:
        return jsonify(False)

@bp.route('/<int:id>',methods=['DELETE'])
def delete(id: int):
    #check if game exists
    g = Game.query.get_or_404(id, "Game not found")
    try:
        db.session.delete(g) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)