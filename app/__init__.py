# app/__init__.py

import datetime
import logging
import os
import secrets
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, request, g
from flask_cors import CORS

from app.api import api_blueprint
from common.models import db
from common.utils.jwt_token import verify_token
from common.utils.output import error


# 配置日志
def configure_logging(app):
    # 清除所有已存在的处理器（非常关键）
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)

    # 获取当前日期
    current_date = datetime.datetime.now()
    current_month = current_date.strftime('%Y-%m')
    current_day = current_date.strftime('%Y-%m-%d')

    # 获取配置中的日志目录和等级
    log_folder_root = app.config.get('LOG_FOLDER', 'logs')
    log_level = app.config.get('LOG_LEVEL', logging.DEBUG)

    # 创建日志文件夹和文件路径
    log_folder = os.path.join(log_folder_root, current_month)
    log_file = os.path.join(log_folder, f"{current_day}.log")

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # 配置文件日志处理器
    file_handler = TimedRotatingFileHandler(
        log_file, when='midnight', interval=1, backupCount=30, encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 配置控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 避免重复添加处理器
    if not app.logger.handlers:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(console_handler)

    app.logger.setLevel(log_level)


# 创建 Flask app
def create_app(config=None):
    if config is None:
        import config

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, static_folder=static_dir)
    app.config.from_object(config)

    # Session Cookie 设置（支持跨域带 cookie）
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='None',
        SESSION_COOKIE_SECURE=False,  # 本地 HTTP 调试必须是 False
    )

    app.secret_key = secrets.token_hex(16)
    db.init_app(app)
    app.register_blueprint(api_blueprint)

    # CORS 设置：允许指定前端域名跨域 + 携带 cookie
    # CORS 配置（必须精确匹配前端域名）
    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:5173"],  # 不能是 * 或省略
        allow_headers=["Content-Type", "Authorization", "lang", "captcha-id"],
        expose_headers=['Captcha-Id']
    )
    # CORS(app, supports_credentials=True)

    configure_logging(app)

    @app.before_request
    def before_request():
        """
        全局请求拦截器
        """
        print(request.endpoint, request)

        # 跳过OPTIONS请求和特定路由
        if request.method == 'OPTIONS' or request.endpoint in [
            'route_map',
            'api.upload',
            'api.get_captcha',
            'api.login',
            'api.register',
            'static'
        ]:
            return

        # Token验证
        authorization = request.headers.get("Authorization")
        auth_header = authorization.replace("Bearer ", "") if authorization else None
        if not auth_header:
            return error(message='No authentication token provided.', code=401)
        try:
            result = verify_token(auth_header)
            # 将用户信息存入g对象
            g.uid = result.get('id')
            g.email = result.get('email')
        except Exception as e:
            return error(message=str(e), code=401)

    return app
