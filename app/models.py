from enum import Enum
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import click

db = SQLAlchemy()

class User(db.Model):

    name = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return '<User name={!r}>'.format(self.name)

class Fridge(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Fridge id={!r}>'.format(self.id)

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    fridge_id = db.Column(db.Integer, db.ForeignKey('fridge.id'), nullable=False)
    fridge = db.relationship('Fridge', backref=db.backref('items', lazy=True))

    def __repr__(self):
        return '<Item id={!r} name={!r}>'.format(self.id, self.name)

class Action(db.Model):

    class Type(Enum):
        PUT = 1
        GET = 2

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(Type), nullable=False)
    time = db.Column(db.DateTime, nullable=False) # UTC time zone
    user_name = db.Column(db.String(64), db.ForeignKey('user.name'), nullable=False)
    user = db.relationship('User')
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item')
    picture = db.deferred(db.Column(db.LargeBinary))

    def __repr__(self):
        return '<Action id={!r} type={!r} time={!r}>'.format(self.id, self.type, self.time)

@click.command('init-db')
@with_appcontext
def init_db():
    db.create_all()
    user = User(name='qianwang', password='424242')
    db.session.add(user)
    fridge = Fridge()
    db.session.add(fridge)
    db.session.commit()
    click.echo('Initialized DB')
