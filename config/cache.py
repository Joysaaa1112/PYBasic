from config import DEBUG

if DEBUG:
    HOST = '127.0.0.1'
    PORT = 6379
    PASSWORD = None
    DB = 0
else:
    HOST = '47.238.224.64'
    PORT = 6379
    PASSWORD = 'momaking'
    DB = 2
