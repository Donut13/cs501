from .models import db, Fridge, Item, Action
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file, render_template, redirect
import base64
import io

root = Blueprint('root', __name__)

def _authenticate(user):
    pass

@root.route('/fridges', methods=['GET'])
def fridges():
    fridges = Fridge.query.all()
    if request.accept_mimetypes.accept_html:
        return render_template('fridges.html', fridges=fridges)
    return jsonify([{'fridge_id': fridge.id} for fridge in fridges])

@root.route('/fridges/<int:fridge_id>/items', methods=['GET', 'POST'])
def fridge_items(fridge_id):
    if request.method == 'GET':
        items = Fridge.query.get(fridge_id).items
        if request.accept_mimetypes.accept_html:
            return render_template('items.html', items=items)
        return jsonify([{'id': item.id, 'name': item.name} for item in items])
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

@root.route('/fridges/<int:fridge_id>/actions', methods=['GET'])
def fridge_actions(fridge_id):
    actions = [
        {
            'id': action.id,
            'type': action.type.name,
            'user': action.user.name,
            'item': action.item.name,
            'time': action.time,
            'has_picture': has_picture,
        }
        for action, has_picture in db.session.query(
            Action, Action.picture != None
        ).join(Action.item).filter(
            Item.fridge_id == fridge_id
        ).order_by(Action.time.desc()).all()
    ]
    return render_template('actions.html', actions=actions)

@root.route('/items/<int:item_id>', methods=['DELETE'])
def item(item_id):
    user = request.json['user']
    _authenticate(user)
    action = Action(type=Action.Type.GET, time=datetime.utcnow(),
                    user_name=user['name'], item_id=item_id)
    db.session.add(action)
    db.session.delete(Item.query.get(item_id))
    db.session.commit()
    return jsonify({'action_id': action.id})

@root.route('/actions/<int:action_id>/picture', methods=['GET', 'PUT'])
def action_picture(action_id):
    action = Action.query.get(action_id)
    if request.method == 'PUT':
        action.picture = base64.decodebytes(bytes(request.data))
        db.session.commit()
        return ('', 204)
    else:
        assert request.method == 'GET'
        return send_file(io.BytesIO(action.picture), mimetype='image/jpeg')

@root.route('/', methods=['GET'])
def index():
    return redirect('/fridges')
