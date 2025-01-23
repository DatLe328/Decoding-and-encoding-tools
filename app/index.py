from flask import Flask, render_template
from app import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/caesar')
def caesar_process():
    return render_template('caesar.html')


@app.route('/vigenere')
def vigenere_process():
    return render_template('vigenere.html')


@app.route('/playfair')
def playfair_process():
    return render_template('playfair.html')


@app.route('/affine')
def affine_process():
    return render_template('affine.html')



@app.route('/hill')
def hill_process():
    return render_template('hill.html')


@app.route('/rsa')
def rsa_process():
    return render_template('rsa.html')



@app.route('/difie-hellman')
def difie_hellman_process():
    return render_template('difie_hellman.html')


if __name__=='__main__':
    app.run(debug=True)