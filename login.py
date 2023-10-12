from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
import datetime
import pymongo
import logging

# 데이터베이스 연결 전역 변수로 선언
mongo_client = pymongo.MongoClient("localhost", 27017)
db = mongo_client["jungle_db"]
users_collection = db["jungle_users"]

# Blueprint 초기화 및 로그 설정
login_bp = Blueprint('login', __name__)
logger = logging.getLogger(__name__)  # 로거 생성

# 라우트 설정


@login_bp.route('/api/v1/login', methods=['POST'])
def login():
    user_id = request.form.get('id')
    password = request.form.get('password')

    # Request 로깅
    logger.info(f"Received ID: {user_id}, Password: {password}")

    user = users_collection.find_one({"id": user_id})

    # MongoDB 쿼리 로깅
    if user:
        logger.info(f"Found user: {user['id']}")
    else:
        logger.warning("No user found in the database.")

    if not user:
        logger.error("아이디를 찾을 수 없습니다.")
        return jsonify({"message": "아이디를 찾을 수 없습니다."}), 401

    if not password:
        logger.error("비밀번호를 입력해주세요.")
        return jsonify({"message": "비밀번호를 입력해주세요."}), 401

    if not check_password_hash(user['password'], password):
        logger.error("비밀번호가 잘못되었습니다.")
        return jsonify({"message": "비밀번호가 잘못되었습니다."}), 401

    # current_app을 사용하여 앱 설정에 접근
    token = jwt.encode({
        'user_id': user["id"],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'])

    # 로그인 성공 메시지 반환
    logger.info("로그인 성공")
    return jsonify({"message": "로그인 하였습니다.", "token": token, "name": user["name"]}), 200
