import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


database_url = "postgresql://disco3_db_user:QrCuxVUzm6JnmTHiM4fLjSSLJXhOpBth@dpg-db59fijbc2fs73epg76g-a.virginia-postgres.render.com/disco3_db"

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eCommerce.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    price = db.Column(db.Numeric(6))
    description = db.Column(db.String(300))
    type = db.Column(db.String(30))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "type": self.type
        }


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data.get("name"),
        price=data.get("price"),
        description=data.get("description"),
        type=data.get("type")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)
    product.type = data.get("type", product.type)
    db.session.commit()
    return jsonify(product.to_dict())

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product was deleted"})


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)