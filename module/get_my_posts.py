from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from functools import wraps
import jwt
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]

get_my_posts_bp = Blueprint('get_my_posts', __name__)
SECRET_KEY = 'your_secret_key_for_jwt'


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")

        if not token:
            return jsonify({"message": "토큰이 없습니다."}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = data['id']
        except:
            return jsonify({"message": "토큰이 유효하지 않습니다."}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@get_my_posts_bp.route('/api/v1/mypost', methods=['GET'])
@jwt_required
def get_my_posts(current_user):
    posts = list(posts_collection.find({"userId": current_user}))

    if not posts:
        return jsonify({"message": "게시물이 없습니다."}), 404

    # Convert ObjectId to string for JSON serialization
    for post in posts:
        post["_id"] = str(post["_id"])

    return jsonify(posts), 200
