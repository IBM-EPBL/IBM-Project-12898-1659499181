from flask import Flask, request, redirect
from flask import render_template


app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html', name = "login")

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        print(name)
        print(email)
        print(password1)
        print(password2)


    return render_template('register.html', name = "register")
