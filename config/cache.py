from config import DEBUG

if DEBUG:
    HOST = '127.0.0.1'
    PORT = 6379
    PASSWORD = None
    DB = 0
else:
    HOST = ''
    PORT = 6379
    PASSWORD = ''
    DB = 2
