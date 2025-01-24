from flask import Flask

app = Flask(__name__)
app.secret_key = 'SECRETKEY'
app.config['ALPHABET_SIZE'] = 26