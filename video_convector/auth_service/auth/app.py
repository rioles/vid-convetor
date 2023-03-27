from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for
from typing import Union
from models.user import User
import jwt, datetime, os

app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """ Home page
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> Union[str, tuple]:
    """ Register user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    user_data = {}
    user_data["email"] = email
    user_data["hashed_password"] = password
    print("okay")
    try:
        AUTH.register_user(**user_data)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    user_data = {}
    user_data["email"] = email
    user_data["hashed_password"] = password
    user = User(**user_data)
    if not AUTH.valid_login(user):
        abort(401)
    else:
        user_data["secret"] = os.environ.get("JWT_SECRET")
        user_data["authz"] = True
        return AUTH.create_jwt(**user_data)


@app.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers["Authaurization"]

    if not encoded_jwt:
        return jsonify({"message": "mmissing credentials"}), 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
        )
    except:
        return jsonify({"message": "not authorized"}), 403
    return jsonify({"decoded": decoded}), 200
    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
