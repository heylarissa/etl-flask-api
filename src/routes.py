from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the API!"})


def register_routes(app):
    app.register_blueprint(api_bp)
