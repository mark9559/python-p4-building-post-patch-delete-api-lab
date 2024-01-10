#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    data = request.form.to_dict()
    for key, value in data.items():
        setattr(bakery, key, value)
    db.session.commit()
    return jsonify(bakery.to_dict())

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form.to_dict()
    new_baked_good = BakedGood(**data)
    db.session.add(new_baked_good)
    db.session.commit()
    return jsonify(new_baked_good.to_dict()), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({'message': 'Baked good deleted successfully'})

if __name__ == '__main__':
    app.run(port=5555, debug=True)
