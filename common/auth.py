import jwt
import functools

from datetime import datetime, timedelta
from flask import request, current_app, session

from .code import ResponseCode
from .response import RespMsg


class Auth:
    key = 'super-man$&923dPs%qzq'

    @classmethod
    def generate_access_token(cls, user_id, algorithm: str = 'HS256', expire: float = 2):
        """
        生成access_token
        :param user_id:自定义部分
        :param algorithm:加密算法
        :param expire:过期时间
        :return:
        """

        key = current_app.config.get('SECRET_KEY', cls.key)
        now = datetime.now()
        expire_datetime = now + timedelta(hours=expire)
        access_payload = {
            'expire': expire_datetime,
            'flag': 0,  # 标识是否为一次性token，0是，1不是
            'start_time': now,  # 开始时间
            'issuer': 'charnet1019',  # 签名
            'user_id': user_id
        }

        access_token = jwt.encode(access_payload, key, algorithm=algorithm)

        return access_token

    @classmethod
    def generate_refresh_token(cls, user_id, algorithm: str = 'HS256', fresh: float = 30):
        """
        生成refresh_token
        :param user_id:自定义部分
        :param algorithm:加密算法
        :param fresh:过期时间
        :return:
        """

        key = current_app.config.get('SECRET_KEY', cls.key)
        now = datetime.now()
        expire_datetime = now + timedelta(days=fresh)
        refresh_payload = {
            'expire': expire_datetime,
            'flag': 1,  # 标识是否为一次性token，0是，1不是
            'start_time': now,  # 开始时间
            'issuer': 'charnet1019',  # 签名
            'user_id': user_id
        }

        refresh_token = jwt.encode(refresh_payload, key, algorithm=algorithm)

        return refresh_token

    @classmethod
    def encode_auth_token(cls, user_id: str,
                          expire: float = 2,
                          fresh: float = 30,
                          algorithm: str = 'HS256') -> [str, str]:
        """
        :param user_id: 用户ID
        :param expire: access_token过期时间
        :param fresh:  refresh_token过期时间,刷新access_token使用
        :param algorithm: 加密算法
        :return:
        """

        access_token = cls.generate_access_token(user_id, algorithm, expire)
        refresh_token = cls.generate_refresh_token(user_id, algorithm, expire)

        return access_token, refresh_token

    @classmethod
    def decode_auth_token(cls, token: str):
        """
        验证token
        :param token:
        :return:
        """

        key = current_app.config.get('SECRET_KEY', cls.key)

        try:
            # 取消过期时间验证
            payload = jwt.decode(token, key=key, )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
            return None
        else:
            return payload

    def identify(self, auth_header):
        """
        用户鉴权
        #TODO:暂时只起用户验证的功能,权限未完善
        :return: list
        """
        if auth_header:
            payload = self.decode_auth_token(auth_header)
            if payload is None:
                return False
            if "user_id" in payload and "flag" in payload:
                if payload["flag"] == 1:
                    # 用来获取新access_token的refresh_token无法获取数据
                    return False
                elif payload["flag"] == 0:

                    return payload["user_id"]
                else:
                    # 其他状态暂不允许
                    return False
            else:
                return False
        else:
            return False


def login_required(f):
    """
    登陆保护，验证用户是否登陆
    :param f:
    :return:
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        res = RespMsg()
        token = request.headers.get("Authorization", default=None)
        if not token:
            res.update(code=ResponseCode.PLEASE_SIGN_IN)
            return res.data

        auth = Auth()
        user_name = auth.identify(token)
        if not user_name:
            res.update(code=ResponseCode.PLEASE_SIGN_IN)
            return res.data

        # 获取到用户并写入到session中,方便后续使用
        session["user_name"] = user_name
        return f(*args, **kwargs)

    return wrapper
