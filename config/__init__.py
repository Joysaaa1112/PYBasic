DEBUG = True

# 数据库配置
if DEBUG:
    HOST = '127.0.0.1'
    PORT = '3306'
    USERNAME = 'root'
    PASSWORD = 'root'
    DATABASE = 'resume'
    CHARSET = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset={CHARSET}'
else:
    HOST = ''
    PORT = '3306'
    USERNAME = ''
    PASSWORD = ''
    DATABASE = ''
    CHARSET = 'utf8mb4'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset={CHARSET}'
    SQLALCHEMY_ECHO = False

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

JWT_SECRET_KEY = '1546229ce1e73b3f94e54b93541f8c86'
# creat_tiktok_com = {
#     'HOST': '',
#     'PORT': '3306',
#     'USERNAME': '',
#     'PASSWORD': '',
#     'DATABASE': '',
# }
#
# SQLALCHEMY_BINDS = {
#     'creat_tiktok_com': f'mysql+pymysql://{creat_tiktok_com["USERNAME"]}:{creat_tiktok_com["PASSWORD"]}@{creat_tiktok_com["HOST"]}:{creat_tiktok_com["PORT"]}/{creat_tiktok_com["DATABASE"]}?charset={CHARSET}'
# }
