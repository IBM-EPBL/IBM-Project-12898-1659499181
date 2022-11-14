from flask import Flask, request, redirect
from flask import render_template
from flask_bcrypt import Bcrypt


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
        dob= request.form['dob']

        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(request.form['password1']).decode('utf-8')

        password2 = request.form['password2']
        confirmPasswordCheck = bcrypt.check_password_hash(hashed_password, password2)
        print("Password1: ", password1)
        print("Password2: " , password2)
        print("Confirm ", confirmPasswordCheck)

        if(confirmPasswordCheck == 1):
            print("yes")
        print(name)
        print(email)
        print(password2 )
        print(type(password2))


    return render_template('register.html', name = "register")
