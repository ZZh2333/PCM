import json
import hashlib
from pathlib import Path
from functools import wraps
from flask import request, session, redirect, url_for, flash
from config.config import Config

DATA_FILE = Config.DATA_DIR / "users.json"

def init_auth(app):
    @app.before_request
    def load_users():
        try:
            # 确保数据文件存在
            DATA_FILE.parent.mkdir(parents=True, exist_ok=True)  # 新增父目录创建
            if not DATA_FILE.exists():
                DATA_FILE.write_text('[]', encoding='utf-8')
            users = json.loads(DATA_FILE.read_text(encoding='utf-8'))
            app.config['USERS'] = {u['username']: u for u in users}
        except Exception as e:
            print(f"初始化用户系统失败: {str(e)}")
            raise
def login_required(role="user"):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('auth.login'))
            user_role = session['user']['role']
            if role == "admin" and user_role != "admin":
                flash("权限不足")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated
    return decorator

def register_user(username, password, role="user"):
    users = json.loads(DATA_FILE.read_text())
    if any(u['username'] == username for u in users):
        return False
    
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": hashlib.sha256(password.encode()).hexdigest(),
        "role": role
    }
    users.append(new_user)
    
    # 原子化写入
    temp_file = DATA_FILE.with_suffix('.tmp')
    with open(temp_file, 'w', encoding='utf-8') as f:  # 显式指定编码
        json.dump(users, f, ensure_ascii=False, indent=2)
    temp_file.replace(DATA_FILE)
    
    return True

def login_user(username, password):
    user = next((u for u in app.config['USERS'].values() 
                if u['username'] == username and 
                u['password'] == hashlib.sha256(password.encode()).hexdigest()), None)
    if user:
        session['user'] = {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
        return True
    return False

# 路由定义
from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if login_user(username, password):
            return redirect(url_for('dashboard'))
        flash("用户名或密码错误")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if register_user(username, password):
            flash("注册成功，请登录")
            return redirect(url_for('auth.login'))
        flash("用户名已存在")
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))