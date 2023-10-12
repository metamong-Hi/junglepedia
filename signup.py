from flask import request, jsonify
from werkzeug.security import generate_password_hash


def signup(users_collection, allowed_users):
    user_id = request.json.get('id')
    password = request.json.get('password')
    name = request.json.get('name')

    # 사용자가 이미 존재하는지 확인
    existing_user = users_collection.find_one({"id": user_id})

    if existing_user:
        if existing_user.get("isRegistered", False):
            return jsonify({"status": "failure", "message": "이미 등록된 사용자입니다."}), 403

        # 이미 존재하는 경우 업데이트
        hashed_pw = generate_password_hash(password)
        users_collection.update_one(
            {"id": user_id},
            {"$set": {"password": hashed_pw, "name": name, "isRegistered": True}}
        )
        return jsonify({"status": "success", "message": "회원가입 성공"}), 200
    else:
        # 사용자가 없으면 추가
        if not any(user['id'] == user_id for user in allowed_users):
            return jsonify({"status": "failure", "message": "등록할 수 없는 아이디입니다"}), 403

        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({
            "id": user_id,
            "password": hashed_pw,
            "name": name,
            "isRegistered": True
        })

        return jsonify({"status": "success", "message": "회원가입 불가"}), 201
