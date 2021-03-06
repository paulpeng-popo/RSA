import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP

import argparse
parser = argparse.ArgumentParser(description='RSA encryption python3 version.')
parser.add_argument('path', metavar='file', type=str, help='the file to be encrypted')
args = parser.parse_args()

path = args.path
try:
    f = open(path, 'r')
    data = f.read().encode("utf-8")
except:
    f = open(path, 'rb')
    data = f.read()
    data = base64.b64encode(data)
f.close()

# data = "I met aliens in UFO. Here is the map.".encode("utf-8")
file_out = open("encrypted_data.st", "wb")

recipient_key = RSA.import_key(open("receiver.pem").read())
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
file_out.close()
