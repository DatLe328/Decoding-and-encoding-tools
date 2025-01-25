from flask import Flask, render_template, request, jsonify
from app import app, dao
import numpy as np
import utils

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caesar')
def caesar_process():
    return render_template('caesar.html')

@app.route('/api/caesar/encode', methods=['POST'])
def caesar_encode():
    data = request.json
    text = data['text']
    shift = data['shift']
    result = dao.caesar_cipher(text, shift)
    return jsonify({'encoded': result})

@app.route('/api/caesar/decode', methods=['POST'])
def caesar_decode():
    data = request.json
    text = data['text']
    shift = data['shift']
    result = dao.caesar_cipher(text, shift, decode=True)
    return jsonify({'decoded': result})



@app.route('/vigenere')
def vigenere_process():
    return render_template('vigenere.html')

@app.route('/api/vigenere/encode', methods=['POST'])
def encode_vigenere():
    data = request.json
    text = data.get('text', '')
    key1 = data.get('key1', '')
    key2 = data.get('key2', None) 

    if not text or not key1:
        return jsonify({'error': 'Text and key1 are required.'}), 400

    if key2:
        result = dao.vigenere_double_cipher(text, key1, key2, decode=False)
    else:
        result = dao.vigenere_cipher(text, key1, decode=False)

    return jsonify({'encoded': result})


@app.route('/api/vigenere/decode', methods=['POST'])
def decode_vigenere():
    data = request.json
    text = data.get('text', '')
    key1 = data.get('key1', '')
    key2 = data.get('key2', None)  

    if not text or not key1:
        return jsonify({'error': 'Text and key1 are required.'}), 400

    if key2:
        result = dao.vigenere_double_cipher(text, key1, key2, decode=True)
    else:
        result = dao.vigenere_cipher(text, key1, decode=True)

    return jsonify({'decoded': result})


@app.route('/playfair')
def playfair_process():
    return render_template('playfair.html')

@app.route('/api/playfair/encode', methods=['POST'])
def encode_playfair():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', '')

    if not text or not key:
        return jsonify({'error': 'Text and key are required.'}), 400

    encoded = dao.playfair_cipher(text, key, decode=False)
    return jsonify({'encoded': encoded})

@app.route('/api/playfair/decode', methods=['POST'])
def decode_playfair():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', '')

    if not text or not key:
        return jsonify({'error': 'Text and key are required.'}), 400

    decoded = dao.playfair_cipher(text, key, decode=True)
    return jsonify({'decoded': decoded})


@app.route('/affine')
def affine_process():
    return render_template('affine.html')

@app.route('/api/affine/encode', methods=['POST'])
def encode_affine():
    data = request.json
    text = data.get('text', '')
    a = data.get('a_coefficient', 0)
    b = data.get('b_coefficient', 0)

    if not text or not isinstance(a, int) or not isinstance(b, int):
        return jsonify({'error': 'Invalid input. Provide text, a, and b.'}), 400
    
    try:
        encoded = dao.affine_encrypt(text, a, b)
        return jsonify({'encoded': encoded})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/affine/decode', methods=['POST'])
def decode_affine():
    data = request.json
    text = data.get('text', '')
    a = data.get('a_coefficient', 0)
    b = data.get('b_coefficient', 0)

    if not text or not isinstance(a, int) or not isinstance(b, int):
        return jsonify({'error': 'Invalid input. Provide text, a, and b.'}), 400
    
    try:
        decoded = dao.affine_decrypt(text, a, b)
        return jsonify({'decoded': decoded})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/hill')
def hill_process():
    return render_template('hill.html')

@app.route('/api/hill/encode', methods=['POST'])
def encode_hill():
    data = request.json
    text = data.get("text", "").replace(" ", "").upper()
    key_matrix = data.get("key_matrix")
    order = data.get("order", "kx")

    try:
        encoded_text = dao.hill_cipher_encode(text, key_matrix, order)
        return jsonify({"encoded": encoded_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/hill/decode', methods=['POST'])
def decode_hill():
    data = request.json
    text = data.get("text", "").replace(" ", "").upper()
    key_matrix = data.get("key_matrix")
    order = data.get("order", "kx")

    try:
        decoded_text = dao.hill_cipher_decode(text, key_matrix, order)
        return jsonify({"decoded": decoded_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/rsa')
def rsa_process():
    return render_template('rsa.html')

@app.route('/api/rsa/generate-keys', methods=['POST'])
def generate_keys_endpoint():
    data = request.json
    p = int(data.get("p", 0))
    q = int(data.get("q", 0))
    e = int(data.get("e", 0))

    if not (utils.isprime(p) and utils.isprime(q)):
        return jsonify({"error": "p và q phải là số nguyên tố."}), 400

    try:
        global keys
        keys = dao.generate_keys(p, q, e)
        print(keys)
        return jsonify({"keys": keys})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

@app.route('/api/rsa/encode', methods=['POST'])
def encode_rsa():
    data = request.json
    text = data.get("text", "")

    if not keys.get("public"):
        return jsonify({"error": "Chưa sinh khóa RSA."}), 400

    e, n = keys["public"]
    encrypted = [pow(ord(char), e, n) for char in text]
    print(encrypted)
    return jsonify({"encoded": " ".join(map(str, encrypted))})

@app.route('/api/rsa/decode', methods=['POST'])
def decode_rsa():
    data = request.json
    text = data.get("text", "")

    if not keys.get("private"):
        return jsonify({"error": "Chưa sinh khóa RSA."}), 400

    d, n = keys["private"]
    try:
        encrypted_numbers = list(map(int, text.split()))
        decrypted = "".join(chr(pow(num, d, n)) for num in encrypted_numbers)
        return jsonify({"decoded": decrypted})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400
@app.route('/difie-hellman')


def difie_hellman_process():
    return render_template('difie_hellman.html')


@app.route('/api/diffie-hellman/exchange', methods=['POST'])
def exchange_keys():
    data = request.json
    p = int(data.get("p"))
    g = int(data.get("g"))
    privateKeyA = int(data.get("privateKeyA"))
    privateKeyB = int(data.get("privateKeyB"))

    try:
        publicKeyA, publicKeyB, sharedKey = dao.diffie_hellman(p, g, privateKeyA, privateKeyB)
        return jsonify({
            "publicKeyA": publicKeyA,
            "publicKeyB": publicKeyB,
            "sharedKey": sharedKey
        })
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


if __name__=='__main__':
    app.run(debug=True)