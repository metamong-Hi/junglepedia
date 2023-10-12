from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import jwt
from functools import wraps

client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]

like_post_bp = Blueprint('like_post', __name__)

SECRET_KEY = 'your_secret_key_for_jwt'


def is_valid_objectid(str_id):
    """Check if a string is a valid ObjectId."""
    try:
        ObjectId(str_id)
        return True
    except:
        return False


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


@like_post_bp.route('/api/v1/like/<postId>', methods=['PUT'])
@jwt_required
def like_post(current_user, postId):
    if not is_valid_objectid(postId):
        return jsonify({"message": "유효하지 않은 postId입니다."}), 400

    userId = current_user

    post = posts_collection.find_one({"_id": ObjectId(postId)})
    if not post:
        return jsonify({"message": "게시물을 찾을 수 없습니다."}), 404

    like_data = likes_collection.find_one(
        {"post": ObjectId(postId), "user": userId})

    if like_data:
        likes_collection.delete_one({"post": ObjectId(postId), "user": userId})
        posts_collection.update_one(
            {"_id": ObjectId(postId)}, {"$inc": {"like": -1}})
        return jsonify({"status": "unliked"}), 200
    else:
        likes_collection.insert_one({"post": ObjectId(postId), "user": userId})
        posts_collection.update_one(
            {"_id": ObjectId(postId)}, {"$inc": {"like": 1}})
        return jsonify({"status": "liked"}), 200
