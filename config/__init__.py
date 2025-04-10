from urllib import parse

DEBUG = False

# 数据库配置
if DEBUG:
    HOST = '127.0.0.1'
    PORT = '3306'
    USERNAME = 'root'
    PASSWORD = 'root'
    DATABASE = 'momaking'
    CHARSET = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset={CHARSET}'
else:
    HOST = '47.238.224.64'
    PORT = '3306'
    USERNAME = 'momaking'
    PASSWORD = 'XwERDh4EbsapbBtK'
    DATABASE = 'momaking'
    CHARSET = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset={CHARSET}'
    SQLALCHEMY_ECHO = False

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
creat_tiktok_com = {
    'HOST': '8.212.144.40',
    'PORT': '3306',
    'USERNAME': 'creat.tiktok.com',
    'PASSWORD': 'TRhAeAAsxkA8rCmJ',
    'DATABASE': 'creat.tiktok.com',
}

SQLALCHEMY_BINDS = {
    'creat_tiktok_com': f'mysql+pymysql://{creat_tiktok_com["USERNAME"]}:{creat_tiktok_com["PASSWORD"]}@{creat_tiktok_com["HOST"]}:{creat_tiktok_com["PORT"]}/{creat_tiktok_com["DATABASE"]}?charset={CHARSET}'
}
