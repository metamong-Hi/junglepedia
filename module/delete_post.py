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

delete_post_bp = Blueprint('delete_post', __name__)
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


@delete_post_bp.route('/api/v1/post/<postId>', methods=['DELETE'])
@jwt_required
def delete_post(current_user, postId):
    post = posts_collection.find_one({"_id": ObjectId(postId)})

    if not post:
        return jsonify({"status": "failure", "message": "글을 찾을 수 없습니다."}), 404

    # 게시물의 작성자와 현재 로그인한 사용자의 ID가 일치하는지 확인
    if post['userId'] != current_user:
        return jsonify({"status": "failure", "message": "권한이 없습니다."}), 403

    result = posts_collection.delete_one({"_id": ObjectId(postId)})

    if result.deleted_count == 0:
        return jsonify({"status": "failure", "message": "글을 찾을 수 없습니다."}), 404

    return jsonify({"status": "success", "message": "글이 성공적으로 삭제되었습니다."}), 200
