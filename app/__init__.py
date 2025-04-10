from flask import Flask
from flask_cors import CORS
import logging
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler
import os
import datetime
from app.api import api_blueprint
from common.models import db


# 配置日志
def configure_logging(app):
    # 获取当前日期
    current_date = datetime.datetime.now()
    current_month = current_date.strftime('%Y-%m')
    current_day = current_date.strftime('%Y-%m-%d')

    # 创建日志文件夹和文件路径
    log_folder = os.path.join('logs', current_month)
    log_file = os.path.join(log_folder, f"{current_day}.log")

    # 创建日志文件夹
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # 配置日志记录到文件
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=30)
    file_handler.setLevel(logging.DEBUG)  # 设置为 DEBUG，记录所有级别的日志
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(file_handler)

    # 配置控制台日志输出
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(handler)

    app.logger.setLevel(logging.DEBUG)


# 创建app
def create_app(config=None):
    if config is None:
        import config
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(api_blueprint)
    CORS(app, supports_credentials=True)

    # 配置日志
    configure_logging(app)
    app.logger.critical("This is a critical message")

    return app
