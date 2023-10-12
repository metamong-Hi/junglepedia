from flask import Blueprint, jsonify
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]

view_most_liked_posts_bp = Blueprint('view_most_liked', __name__)


@view_most_liked_posts_bp.route('/api/v1/view/like/<category>', methods=['GET'])
def view_most_liked_posts(category):
    posts = list(posts_collection.find(
        {"category": category}).sort("like", -1).limit(30))

    if not posts:
        return jsonify({'status': 'fail', 'message': '글없다'}), 500

    for post in posts:
        post["_id"] = str(post["_id"])

    return jsonify({'posts': posts, 'status': 'success', 'message': '불러오기성공'}), 200
