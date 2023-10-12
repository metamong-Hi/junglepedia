from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import pandas as pd
import logging
import jwt
# from module import (login)
from init_db import initialize_db
from module.signup import signup as signup_func
from module import (login, logout, create_post, get_my_posts, delete_post,
                    like_post, update_post, view_most_liked_posts, view_recent_posts)
app = Flask(__name__)

# 로거 생성 및 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 로그 레벨 설정

# 콘솔 출력 핸들러 설정
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 로그 포맷 설정
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 핸들러를 로거에 추가
logger.addHandler(ch)

SECRET_KEY = 'your_secret_key'  # JWT 토큰과 Flask 앱 설정에 사용될 SECRET_KEY


@app.route('/api/v1/verify_token', methods=['POST'])
def verify_token():
    token = request.json.get('token')

    if not token:
        return jsonify({'result': 'fail', 'message': '토큰이 제공되지 않았습니다.'}), 400

    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'result': 'success', 'message': '토큰이 유효합니다.', 'payload': decoded_payload}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'message': '토큰이 만료되었습니다.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'result': 'fail', 'message': '유효하지 않은 토큰입니다.'}), 401


app.config['SECRET_KEY'] = SECRET_KEY  # Flask 앱 설정에 SECRET_KEY 설정

# MongoDB 설정 및 데이터베이스 연결을 앱의 컨텍스트에 저장
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["USERS"]
posts_collection = db["POSTS"]
likes_collection = db["LIKES"]

# 엑셀 파일에서 'id', 'name' 정보 가져오기
df = pd.read_excel(
    r"C:\Users\User\Desktop\hey\Jungle_DB.xlsx")


@app.route('/')
def index():
    # 루트 경로에 대한 처리
    return render_template('index.html')


@app.route('/home')
def home():
    # 루트 경로에 대한 처리
    return render_template('home.html')


@app.route('/signin')
def signin():
    # 루트 경로에 대한 처리
    return render_template('signin.html')


@app.route('/register')
def register():
    # 루트 경로에 대한 처리
    return render_template('register.html')


@app.route('/mypage')
def mypage():
    # 루트 경로에 대한 처리
    return render_template('mypage.html')


@app.route('/post_real')
def post():
    # 루트 경로에 대한 처리
    return render_template('post_real.html')


@app.route('/real_update')
def real_update():
    return render_template('update.html')


@app.route('/week1')
def week1():
    # 루트 경로에 대한 처리
    return render_template('week1.html')


@app.errorhandler(404)
def page_not_found(e):
    return "페이지를 찾을 수 없습니다. 요청한 URL이 잘못되었을 수 있습니다.", 404


@app.route('/api/v1/signup', methods=['POST'])
def signup_route():
    """회원 가입 라우트"""
    return signup_func()


@app.errorhandler(404)
def page_not_found(e):
    return "페이지를 찾을 수 없습니다. 요청한 URL이 잘못되었을 수 있습니다.", 404


# 블루프린트 등록
app.register_blueprint(login.login_bp)
app.register_blueprint(logout.logout_bp)
app.register_blueprint(create_post.create_post_bp)
app.register_blueprint(get_my_posts.get_my_posts_bp)
app.register_blueprint(delete_post.delete_post_bp)
app.register_blueprint(like_post.like_post_bp)
app.register_blueprint(update_post.update_post_bp)
app.register_blueprint(view_most_liked_posts.view_most_liked_posts_bp)
app.register_blueprint(view_recent_posts.view_recent_posts_bp)
if __name__ == '__main__':
    initialize_db()
    app.run('0.0.0.0', port=5000, debug=True)
