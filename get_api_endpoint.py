import json
import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "price_data.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

db = SQLAlchemy(app)


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    hour = db.Column(db.Integer)
    price = db.Column(db.Float)
    volume = db.Column(db.Float)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "hour": self.hour,
            "price": self.price,
            "volume": self.volume
        }


@app.route("/pricing/search/<date>", methods=["GET"])
def get_pricing(date) -> json:
    date_obj = datetime.strptime(date, "%d.%m.%Y").date()

    pricings = Price.query.filter_by(date=date_obj).all()
    if not pricings:
        return jsonify({"error": "No pricing data found for the specified date"}), 404

    pricings_list = [pricing.to_dict() for pricing in pricings]
    return jsonify(pricings_list)


if __name__ == "__main__":
    app.run()
