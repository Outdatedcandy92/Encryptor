from flask import Flask, request, render_template, render_template_string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
app = Flask(__name__)

def Encrypt(text_data, key):
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
    print(encoded_text)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_text():
    print(request.form)  # Debugging line
    text_data = request.form['text']
    key = request.form['Pass']
    encrypted_text = Encrypt(text_data, key)
    return render_template('index.html',encout=encrypted_text)

app.run(host='0.0.0.0', port=8080)