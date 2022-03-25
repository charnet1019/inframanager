import base64
import functools
import io
import random
import string
import redis

from flask import current_app

from PIL import Image, ImageFont, ImageDraw

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

import pandas as pd
from flask import make_response, request


def gen_cert():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)

    private_key = rsa.exportKey()
    public_key = rsa.public_key().exportKey()


def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)

    return key


def encrypt_msg(msg):
    public_key = get_key('cert/public_key.pem')
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode('utf-8'))))

    return encrypt_text.decode('utf-8')


def decrypt_msg(msg):
    private_key = get_key('cert/private_key.pem')
    cipher = PKCS1_cipher.new(private_key)
    plain_text = cipher.decrypt(base64.b64decode(msg), 0)

    return plain_text.decode('utf-8')


def sign(data):
    private_key = get_key('cert/private_key.pem')
    signer = PKCS1_signature.new(private_key)
    digest = SHA.new()
    digest.update(data.encode('utf-8'))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    signature = signature.decode('utf-8')

    return signature


def check_sign(text, sign):
    public_key = get_key('cert/public_key.pem')
    verifier = PKCS1_signature.new(public_key)
    digest = SHA.new()
    digest.update(text.encode("utf8"))

    return verifier.verify(digest, base64.b64decode(sign))


def export_data(column, data):
    bio = io.BytesIO()
    writer = pd.ExcelWriter(bio, engine='xlsxwriter')
    # writer = pd.ExcelWriter(bio)

    df = pd.DataFrame(columns=column, data=data)
    df.to_excel(excel_writer=writer, sheet_name='主机信息', index=False)
    writer.save()
    bio.seek(0)
    ret = make_response(bio.getvalue())
    bio.close()

    ret.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ret.headers["Cache-Control"] = "no-cache"
    ret.headers['Content-Disposition'] = 'attachment; filename={}.xlsx'.format('hostinfo')

    return ret


class Captcha:
    """
    生成图片验证码
    """

    def __init__(self, width=50, height=12):
        self.width = width
        self.height = height

        self.im = Image.new('RGB', (width, height), 'white')
        self.font = ImageFont.load_default()
        self.draw = ImageDraw.Draw(self.im)

    def draw_lines(self, num=3):
        for num in range(num):
            x1 = random.randint(0, self.width / 2)
            y1 = random.randint(0, self.height / 2)
            x2 = random.randint(0, self.width)
            y2 = random.randint(self.height / 2, self.height)

            self.draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

    def get_verify_code(self):
        """
        生成验证码图形
        :return:
        """

        code = ''.join(random.sample(string.digits, 4))
        # 绘制字符串
        for item in range(len(code)):
            self.draw.text((6 + random.randint(-3, 3) + 10 * item, 2 + random.randint(-2, 2)),
                           text=code[item],
                           fill=(random.randint(32, 127),
                                 random.randint(32, 127),
                                 random.randint(32, 127)),
                           font=self.font)

        # 划线
        self.draw_lines()
        # 重新设置图片大小
        self.im = self.im.resize((100, 24))
        # 图片转换为base64
        buffered = io.BytesIO()
        self.im.save(buffered, format='JPEG')
        img_str = b'data:image/png;base64,' + base64.b64encode(buffered.getvalue())

        return img_str, code


class Redis:
    """
    redis数据库操作
    """

    @staticmethod
    def _get_conn():
        host = current_app.config['REDIS_HOST']
        port = current_app.config['REDIS_PORT']
        db = current_app.config['REDIS_DB']
        password = current_app.config['REDIS_PASSWORD']

        if password:
            r = redis.StrictRedis(host=host, port=port, db=db, password=password)
        else:
            r = redis.StrictRedis(host=host, port=port, db=db)

        return r

    @classmethod
    def write(cls, key, value, expire=None):
        """
        写入键值对
        :param key:
        :param value:
        :param expire:
        :return:
        """

        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = current_app.config['REDIS_EXPIRE']

        r = cls._get_conn()
        r.set(key, value, ex=expire_in_seconds)

    @classmethod
    def read(cls, key):
        """
        读取键值对内容
        :param key:
        :return:
        """

        r = cls._get_conn()
        value = r.get(key)

        return value.decode('utf-8') if value else value

    @classmethod
    def hset(cls, name, key, value):
        """
        写入hash表
        :param name:
        :param key:
        :param value:
        :return:
        """

        r = cls._get_conn()
        r.hset(name, key, value)

    @classmethod
    def hmset(cls, key, *value):
        """
        读取指定hash表的所有给定字段的值
        :param key:
        :param value:
        :return:
        """

        r = cls._get_conn()
        value = r.hmset(key, *value)

        return value

    @classmethod
    def hget(cls, name, key):
        """
        读取指定hash表的键值
        :param name:
        :param key:
        :return:
        """

        r = cls._get_conn()
        value = r.hget(name, key)

        return value.decode('utf-8') if value else value

    @classmethod
    def hgetall(cls, name):
        """
        获取指定hash表所有的值
        :param name:
        :return:
        """

        r = cls._get_conn()
        return r.hgetall(name)

    @classmethod
    def delete(cls, *names):
        """
        删除一个或者多个
        :param names:
        :return:
        """

        r = cls._get_conn()
        r.delete(*names)

    @classmethod
    def hdel(cls, name, key):
        """
        删除指定hash表的键值
        :param name:
        :param key:
        :return:
        """

        r = cls._get_conn()
        r.hdel(name, key)

    @classmethod
    def expire(cls, name, expire=None):
        """
        设置过期时间
        :param name:
        :param expire:
        :return:
        """

        if expire:
            expire_in_seconds = expire
        else:
            expire_in_seconds = current_app.config['REDIS_EXPIRE']

        r = cls._get_conn()
        r.expire(name, expire_in_seconds)


if __name__ == '__main__':
    # with open('../cert/private_key.pem', 'wb') as f:
    #     f.write(private_key)
    #
    # with open('../cert/public_key.pem', 'wb') as f:
    #     f.write(public_key)

    enc_text = encrypt_msg('123456')
    print(enc_text)
    print(decrypt_msg(enc_text))
