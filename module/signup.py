from flask import request, jsonify
from werkzeug.security import generate_password_hash
from pymongo import MongoClient


# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]


def signup():
    user_id = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')

    # 필수 데이터 확인
    if not all([user_id, password, name]):
        return jsonify({"status": "failure", "message": "아이디, 비밀번호, 이름을 모두 입력해주세요."}), 400

    # 사용자가 목록에 있는지 확인
    existing_user = users_collection.find_one({"id": user_id})
    if not existing_user:
        return jsonify({"status": "failure", "message": "등록할 수 없는 아이디입니다. 정글 입학시 사용한 이메일을 입력해주세요."}), 403
    if existing_user.get("isRegistered", False):  # 'isRegistered' 필드 값이 True일 경우 실행
        return jsonify({"status": "failure", "message": "이미 등록된 사용자입니다."}), 403

    # 이름 일치 여부 확인
    if existing_user["name"] != name:
        return jsonify({"status": "failure", "message": "이름이 일치하지 않습니다."}), 403

    # 비밀번호를 'scrypt' 방식으로 해시화
    hashed_pw = generate_password_hash(password, method='scrypt')

    # 사용자 데이터 업데이트
    users_collection.update_one(
        {"id": user_id},
        {"$set": {"password": hashed_pw, "isRegistered": True}}
    )
    print("(가입) 이름:", name, "/ 이메일:", user_id, "/ 비밀번호:", password)
    return jsonify({"status": "success", "message": "회원가입 성공"}), 200
