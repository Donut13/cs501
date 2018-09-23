from .models import db, Fridge, Item, Action, User
from datetime import datetime
from flask import Blueprint, request, jsonify, abort, send_file
import io

root = Blueprint('root', __name__)

def _authenticate(user):
    u = User.query.get(user['name'])
    if u is None or u.password != user['password']: abort(401)

@root.route('/fridges', methods=['GET'])
def fridges():
    return jsonify([{'fridge_id': fridge.id} for fridge in Fridge.query.all()])

@root.route('/fridges/<int:fridge_id>/items', methods=['GET', 'POST'])
def fridge_items(fridge_id):
    if request.method == 'GET':
        return jsonify([{'id': item.id, 'name': item.name}
                        for item in Fridge.query.get(fridge_id).items])
    else:
        assert request.method == 'POST'
        user = request.json['user']
        _authenticate(user)
        item = Item(name=request.json['item_name'], fridge_id=fridge_id)
        db.session.add(item)
        db.session.flush()
        action = Action(type=Action.Type.PUT, time=datetime.utcnow(),
                        user_name=user['name'], item_id=item.id)
        db.session.add(action)
        db.session.commit()
        return jsonify({'action_id': action.id})

@root.route('/items/<int:item_id>', methods=['DELETE'])
def item(item_id):
    user = request.json['user']
    _authenticate(user)
    action = Action(type=Action.Type.GET, time=datetime.utcnow(),
                    user_name=user['name'], item_id=item_id)
    db.session.add(action)
    db.session.delete(Item.query.get(item_id))
    db.session.commit()
    return ('', 204)

@root.route('/actions/<int:action_id>/picture', methods=['GET', 'PUT'])
def action_picture(action_id):
    action = Action.query.get(action_id)
    if request.method == 'PUT':
        picture = request.files['picture']
        try:
            action.picture = picture.read()
            db.session.commit()
        finally:
            picture.close()
        return ('', 204)
    else:
        assert request.method == 'GET'
        return send_file(io.BytesIO(action.picture), mimetype='image/jpeg')

@root.route('/', methods=['GET'])
def index():
    return 'index'
