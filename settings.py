ENV = 'development'
DEBUG = True
JSON_AS_ASCII = False

# 数据库
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:XpWQ9Hu5S0543WmE@192.168.60.3:3306/inframanager'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False    # 调试模式

# redis
REDIS_HOST = '192.168.60.3'
REDIS_PORT = 6379
REDIS_DB = 5
REDIS_PASSWORD = 'secret'
REDIS_EXPIRE = 3600   # 默认过期时间

# 加载本地静态资源
BOOTSTRAP_SERVE_LOCAL = True

SECRET_KEY = '795c7d00f493489a986f09a100aa1edf'

WTF_CSRF_CHECK_DEFAULT = False

PUBLIC_KEY = 'cert/public_key.pem'
PRIVATE_KEY = 'cert/private_key.pem'
