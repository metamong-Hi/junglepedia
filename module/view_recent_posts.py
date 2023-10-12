from flask import Blueprint, jsonify
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]

view_recent_posts_bp = Blueprint('view_recent', __name__)


@view_recent_posts_bp.route('/api/v1/view/recent/<category>', methods=['GET'])
def view_recent_posts(category):
    posts = list(posts_collection.find(
        {"category": category}).sort("date", -1).limit(30))

    if not posts:
        return jsonify({"message": "해당 카테고리의 게시물이 없습니다."}), 404

    for post in posts:
        post["_id"] = str(post["_id"])

    return jsonify(posts), 200
