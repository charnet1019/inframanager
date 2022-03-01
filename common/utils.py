import base64

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher

random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)

private_key = rsa.exportKey()
public_key = rsa.public_key().exportKey()

def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)

    return key


def encrypt(msg):
    public_key = get_key('cert/public_key.pem')
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(msg.encode('utf-8'))))

    return encrypt_text.decode('utf-8')


def decrypt(encrypt_msg):
    private_key = get_key('cert/private_key.pem')
    cipher = PKCS1_cipher.new(private_key)
    plain_text = cipher.decrypt(base64.b64decode(encrypt_msg), 0)

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
    publick_key = get_key('cert/public_key.pem')
    verifier = PKCS1_signature.new(publick_key)
    digest = SHA.new()
    digest.update(text.encode("utf8"))

    return verifier.verify(digest, base64.b64decode(sign))


if __name__ == '__main__':
    # with open('../cert/private_key.pem', 'wb') as f:
    #     f.write(private_key)
    #
    # with open('../cert/public_key.pem', 'wb') as f:
    #     f.write(public_key)

    enc_text = encrypt('123456')
    print(enc_text)
    print(decrypt(enc_text))
