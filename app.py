from flask import Flask, render_template
from pymongo import MongoClient
import pandas as pd
# from init_db import initialize_db
from signup import signup as signup_func
from login import login as login_func
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# MongoDB 설정
client = MongoClient("mongodb://localhost:27017/")
db = client["jungle_db"]
users_collection = db["jungle_users"]
posts_collection = db["jungle_posts"]

# 엑셀 파일에서 'id', 'name' 정보 가져오기
df = pd.read_excel(
    r"C:\Users\User\Desktop\hey\Jungle_DB.xlsx")

allowed_users = df[['id', 'name']].to_dict(orient='records')


@app.route('/api/v1/signup', methods=['POST'])
def signup_route():
    return signup_func(users_collection, allowed_users)


@app.route('/')
def index():
    # 루트 경로에 대한 처리
    return render_template('index.html')


@app.route('/home')
def home():
    # 루트 경로에 대한 처리
    return render_template('home.html')


@app.route('/login')
def login():
    # 루트 경로에 대한 처리
    return render_template('login.html')


@app.route('/register')
def register():
    # 루트 경로에 대한 처리
    return render_template('register.html')


@app.route('/mypage')
def mypage():
    # 루트 경로에 대한 처리
    return render_template('mypage.html')


@app.route('/post')
def post():
    # 루트 경로에 대한 처리
    return render_template('post.html')


@app.errorhandler(404)
def page_not_found(e):
    return "페이지를 찾을 수 없습니다. 요청한 URL이 잘못되었을 수 있습니다.", 404


# # 블루프린트 등록
# app.register_blueprint(login.login_bp)
# app.register_blueprint(logout.logout_bp)
# app.register_blueprint(create_post.create_post_bp)
# app.register_blueprint(get_my_posts.get_my_posts_bp)
# app.register_blueprint(delete_post.delete_post_bp)
# app.register_blueprint(like_post.like_post_bp)
# app.register_blueprint(update_post.update_post_bp)
# app.register_blueprint(view_most_liked_posts.view_most_liked_posts_bp)
# app.register_blueprint(view_recent_posts.view_recent_posts_bp)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
