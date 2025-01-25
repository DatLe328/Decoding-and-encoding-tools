import numpy as np
import math


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y


def mod_inverse(a, m):
    g, x, y =extended_gcd(a, m)
    if g != 1:
        return None  
    else:
        return x % m


def matrix_mod_inverse(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))
    det_inv = mod_inverse(det % modulus, modulus)

    if det_inv is None:
        raise ValueError("Matrix determinant is not invertible under modulo.")

    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    return (det_inv * adjugate) % modulus


def isprime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True