from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import jwt
from functools import wraps

client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]

update_post_bp = Blueprint('update_post', __name__)
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


@update_post_bp.route('/api/v1/post/<postId>', methods=['PUT'])
@jwt_required
def update_post(current_user, postId):
    post_data = request.json

    post = posts_collection.find_one({"_id": ObjectId(postId)})

    # 게시물이 존재하지 않는 경우
    if not post:
        return jsonify({"message": "게시물을 찾을 수 없습니다."}), 404

    # 현재 사용자가 게시물의 원작성자가 아닌 경우
    if post['userId'] != current_user:
        return jsonify({"message": "이 게시물을 수정할 권한이 없습니다."}), 403

    result = posts_collection.update_one(
        {"_id": ObjectId(postId)}, {"$set": post_data})

    if result.matched_count == 0:
        return jsonify({"status": "failure", "message": "글을 찾을 수 없습니다."}), 404

    if result.modified_count == 0:
        return jsonify({"status": "failure", "message": "글 수정에 실패했습니다."}), 500

    return jsonify({"status": "success", "message": "글이 성공적으로 수정되었습니다."}), 200
