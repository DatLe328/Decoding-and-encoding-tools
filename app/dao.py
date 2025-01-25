from math import gcd
from app import app
import utils, math
import numpy as np

def caesar_cipher(text, shift, decode=False):
    decrypted = ""
    for char in text:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            decrypted += chr((ord(char) - shift_amount 
                              + shift * (-1 if decode else 1)) % 26 + shift_amount)
        else:
            decrypted += char
    return decrypted


def vigenere_cipher(text, key, decode=False):
    result = []
    key = key.upper()
    key_len = len(key)
    key_idx = 0

    for char in text:
        if char.isalpha():
            shift = ord(key[key_idx % key_len]) - ord('A')
            if decode:
                shift = -shift
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)

def vigenere_double_cipher(text, key1, key2, decode=False):
    intermediate = vigenere_cipher(text, key1, decode)
    return vigenere_cipher(intermediate, key2, decode)


def create_playfair_table(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" 
    key = "".join(dict.fromkeys(key.upper().replace("J", "I") + alphabet))
    table = [key[i:i+5] for i in range(0, 25, 5)]
    return table

def find_position(table, char):
    for i, row in enumerate(table):
        if char in row:
            return i, row.index(char)
    return None

def playfair_cipher(text, key, decode=False):
    table = create_playfair_table(key)
    text = text.upper().replace("J", "I")
    pairs = []
    i = 0

    while i < len(text):
        a = text[i]
        if i + 1 < len(text) and text[i + 1] != a:
            b = text[i + 1]
            i += 2
        else:
            b = 'X'
            i += 1
        pairs.append((a, b))

    result = []

    for a, b in pairs:
        row1, col1 = find_position(table, a)
        row2, col2 = find_position(table, b)

        if row1 == row2: 
            shift = -1 if decode else 1
            result.append(table[row1][(col1 + shift) % 5])
            result.append(table[row2][(col2 + shift) % 5])
        elif col1 == col2:  
            shift = -1 if decode else 1
            result.append(table[(row1 + shift) % 5][col1])
            result.append(table[(row2 + shift) % 5][col2])
        else:  
            result.append(table[row1][col2])
            result.append(table[row2][col1])

    return ''.join(result)


def affine_encrypt(text, a, b, mod=app.config['ALPHABET_SIZE']):
    print(a)
    print(mod)
    if gcd(a, mod) != 1:
        raise ValueError("Key 'a' and alphabet size must be coprime.")
    
    encrypted = []
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            x = ord(char) - offset
            encrypted.append(chr(((a * x + b) % mod) + offset))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def affine_decrypt(text, a, b, mod=app.config['ALPHABET_SIZE']):
    if gcd(a, mod) != 1:
        raise ValueError("Key 'a' and alphabet size must be coprime.")
    
    a_inv = utils.mod_inverse(a, mod)
    if a_inv is None:
        raise ValueError("Multiplicative inverse of 'a' does not exist.")
    
    decrypted = []
    for char in text:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            y = ord(char) - offset
            decrypted.append(chr(((a_inv * (y - b)) % mod) + offset))
        else:
            decrypted.append(char)
    return ''.join(decrypted)



def hill_cipher_encode(text, key_matrix, order, mod=26):
    key_matrix = np.array(key_matrix)
    text_vector = [ord(char.upper()) - ord('A') for char in text if char.isalpha()]
    
    n = key_matrix.shape[0]
    while len(text_vector) % n != 0:
        text_vector.append(0) 

    text_vector = np.array(text_vector).reshape(-1, n)
    
    if order == "kx":
        result_vector = np.dot(text_vector, key_matrix.T) % mod
    elif order == "xk":
        result_vector = np.dot(text_vector, key_matrix) % mod
    else:
        raise ValueError("Invalid order. Use 'kx' or 'xk'.")
    result = ''.join(chr(int(num) + ord('A')) for row in result_vector for num in row)
    return result

def hill_cipher_decode(text, key_matrix, order, mod=app.config['ALPHABET_SIZE']):
    key_matrix = np.array(key_matrix)
    n = key_matrix.shape[0]

    det = int(round(np.linalg.det(key_matrix)))
    det_inv = utils.mod_inverse(det, mod)
    key_matrix_inv = det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int) % mod

    text_vector = [ord(char.upper()) - ord('A') for char in text if char.isalpha()]
    text_vector = np.array(text_vector).reshape(-1, n)
    
    if order == "kx":
        result_vector = np.dot(text_vector, key_matrix_inv.T) % mod
    elif order == "xk":
        result_vector = np.dot(text_vector, key_matrix_inv) % mod
    else:
        raise ValueError("Invalid order. Use 'kx' or 'xk'.")

    result = ''.join(chr(int(num) + ord('A')) for row in result_vector for num in row)
    return result


def generate_keys(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)

    if math.gcd(e, phi) != 1:
        raise ValueError("e phải nguyên tố cùng nhau với φ(n).")
    d = utils.mod_inverse(e, phi)
    return {"public": (e, n), "private": (d, n)}


def diffie_hellman(p, g, privateKeyA, privateKeyB):
    publicKeyA = pow(g, privateKeyA, p)
    publicKeyB = pow(g, privateKeyB, p)

    sharedKeyA = pow(publicKeyB, privateKeyA, p)
    sharedKeyB = pow(publicKeyA, privateKeyB, p)

    if sharedKeyA != sharedKeyB:
        raise ValueError("Shared keys do not match!")

    return publicKeyA, publicKeyB, sharedKeyA