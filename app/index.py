from flask import Flask, render_template, request, jsonify
from app import app, dao
import numpy as np

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
def encode():
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
def decode():
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



@app.route('/difie-hellman')
def difie_hellman_process():
    return render_template('difie_hellman.html')


if __name__=='__main__':
    app.run(debug=True)