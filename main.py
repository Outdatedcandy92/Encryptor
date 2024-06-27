from flask import Flask, request, render_template, render_template_string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
app = Flask(__name__)

def Encrypt_AES(text_data, key):
    # Ensure key is 32 bytes (AES-256)
    key = key.encode().ljust(32, b'\0')[:32]
    # Create a new AES cipher
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad the plaintext to be AES block size compliant
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text_data.encode()) + padder.finalize()
    # Encrypt the padded plaintext
    encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
    # Encode the encrypted text to base64
    encoded_text = base64.b64encode(encrypted_text).decode()
    return encoded_text

def Encrypt_DES(text_data, key):
    # Ensure key is 8 bytes (DES)
    key = key.encode().ljust(8, b'\0')[:8]
    # Create a new DES cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad the plaintext to be DES block size compliant
    padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()
    padded_data = padder.update(text_data.encode()) + padder.finalize()
    # Encrypt the padded plaintext
    encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
    # Encode the encrypted text to base64
    encoded_text = base64.b64encode(encrypted_text).decode()
    return encoded_text

def Encrypt_3DES(text_data, key):
    # Ensure key is 24 bytes (3DES)
    key = key.encode().ljust(24, b'\0')[:24]
    # Create a new 3DES cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad the plaintext to be 3DES block size compliant
    padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()
    padded_data = padder.update(text_data.encode()) + padder.finalize()
    # Encrypt the padded plaintext
    encrypted_text = encryptor.update(padded_data) + encryptor.finalize()
    # Encode the encrypted text to base64
    encoded_text = base64.b64encode(encrypted_text).decode()
    return encoded_text

def encrypt_type(text_data, key, opt):
    if opt == "aes":
        return Encrypt_AES(text_data, key)
    elif opt == "des":
        return Encrypt_DES(text_data, key)
    elif opt == "3des":
        return Encrypt_3DES(text_data, key)
    
def decrypt_type(encrypted_data, key, opt):
    if opt == "aes":
        return Decrypt_AES(encrypted_data, key)
    elif opt == "des":
        return Decrypt_DES(encrypted_data, key)
    elif opt == "3des":
        return Decrypt_3DES(encrypted_data, key)

def Decrypt_AES(encrypted_data, key):
    # Ensure key is 32 bytes (AES-256)
    key = key.encode().ljust(32, b'\0')[:32]
    # Create a new AES cipher
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    # Decode the base64 encoded encrypted text
    encrypted_text = base64.b64decode(encrypted_data.encode())
    # Decrypt the encrypted text
    decrypted_data = decryptor.update(encrypted_text) + decryptor.finalize()
    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    # Decode the decrypted data from bytes to string
    decoded_data = unpadded_data.decode()
    return decoded_data

def Decrypt_DES(encrypted_data, key):
    # Ensure key is 8 bytes (DES)
    key = key.encode().ljust(8, b'\0')[:8]
    # Create a new DES cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    # Decode the base64 encoded encrypted text
    encrypted_text = base64.b64decode(encrypted_data.encode())
    # Decrypt the encrypted text
    decrypted_data = decryptor.update(encrypted_text) + decryptor.finalize()
    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    # Decode the decrypted data from bytes to string
    decoded_data = unpadded_data.decode()
    return decoded_data

def Decrypt_3DES(encrypted_data, key):
    # Ensure key is 24 bytes (3DES)
    key = key.encode().ljust(24, b'\0')[:24]
    # Create a new 3DES cipher
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    # Decode the base64 encoded encrypted text
    encrypted_text = base64.b64decode(encrypted_data.encode())
    # Decrypt the encrypted text
    decrypted_data = decryptor.update(encrypted_text) + decryptor.finalize()
    # Unpad the decrypted data
    unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    # Decode the decrypted data from bytes to string
    decoded_data = unpadded_data.decode()
    return decoded_data

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_text():
    print(request.form)  # Debugging line
    text_data = request.form['text']
    key = request.form['Pass']
    opt = request.form['encryptionType']

    data = encrypt_type(text_data,key,opt)

    return render_template('index.html',encout=data)

@app.route('/decrypt', methods=['POST'])
def decrypt_text():
    encrypted_data = request.form['text']
    key = request.form['Pass']
    opt = request.form['encryptionType']
    data = decrypt_type(encrypted_data, key, opt)
    return render_template('index.html', encout=data, operation="decrypt")
    
app.run(host='0.0.0.0', port=8080)