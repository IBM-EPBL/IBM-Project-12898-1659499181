from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html', name = "login")

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    return render_template('register.html')
