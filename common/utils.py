import base64
import io

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

import pandas as pd
from flask import make_response


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


if __name__ == '__main__':
    # with open('../cert/private_key.pem', 'wb') as f:
    #     f.write(private_key)
    #
    # with open('../cert/public_key.pem', 'wb') as f:
    #     f.write(public_key)

    enc_text = encrypt_msg('123456')
    print(enc_text)
    print(decrypt_msg(enc_text))
