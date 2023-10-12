from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import logging

# Blueprint 초기화 및 로그 설정
login_bp = Blueprint('login', __name__)
logger = logging.getLogger(__name__)  # 로거 생성

SECRET_KEY = 'your_secret_key_for_jwt'

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]


@login_bp.route('/api/v1/login', methods=['POST'])
def login():
    id_receive = request.json.get('id')
    pw_receive = request.json.get('password')

    logger.warning("id 및 password를 받았습니다.")
    print(id_receive, pw_receive)

    # 사용자로부터 받은 id 로깅 (비밀번호 로깅은 보안상 제외)
    logger.warning(f"받은 id: {id_receive}")

    if not id_receive or not pw_receive:
        logger.warning("받은 값이 없습니다.")
        return jsonify({'status': 'fail', 'msg': '아이디 또는 비밀번호 정보가 제공되지 않았습니다.'}), 400

    # 주어진 'id'로 바로 사용자를 찾습니다.
    user = users_collection.find_one({"id": id_receive})

    # 사용자가 존재하는지, 제공된 비밀번호가 저장된 비밀번호 해시와 일치하는지 확인합니다.

    # 여기 수정 -->비밀번호 체크
    if user:
        # JWT 토큰 생성
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(days=1)  # 토큰은 1일 후에 만료됩니다.
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        logger.info("로그인 성공")
        return jsonify({'status': 'success', 'token': token, 'message': '로그인 성공', 'id_message': 'id가 있습니다.'}), 200
    else:
        logger.warning("아이디/비밀번호가 일치하지 않습니다.")
        return jsonify({'status': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'}), 401
