from flask import Flask, request, redirect, flash, url_for
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$IBMCloud123!'
app.config['MYSQL_DB'] = 'Web Phishing'
 
mysql = MySQL(app)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        bcrypt = Bcrypt()

        cursor.execute('''SELECT pass FROM user WHERE email = %s''', [email])
        account = cursor.fetchone()

        print("UserPass is ",account[0])
        password = request.form['password']

        confirmPasswordCheck = bcrypt.check_password_hash(account[0], password)
        print("Confirm " , confirmPasswordCheck)


        
 
        # if account:
        #     password_rs = account['password']
        #     print(password_rs)
        #     # If account exists in users table in out database
        #     if check_password_hash(password_rs, password):
        #         # Create session data, we can access this data in other routes
        #         session['loggedin'] = True
        #         session['id'] = account['id']
        #         session['username'] = account['username']
        #         # Redirect to home page
        #         return redirect(url_for('home'))
        #     else:
        #         # Account doesnt exist or username/password incorrect
        #         flash('Incorrect username/password')
        # else:
        #     # Account doesnt exist or username/password incorrect
        #     flash('Incorrect username/password')

        return redirect(url_for('home'))


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
        gender = "M"

        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(request.form['password1']).decode('utf-8')

        cursor = mysql.connection.cursor()


        #Check for existing user
        cursor.execute('''SELECT * FROM user WHERE email = %s''', [email])
        account = cursor.fetchone()
        if account:
            flash('Account already exists!')

        else:
            cursor.execute(''' INSERT INTO User VALUES(%s,%s,%s,%s,%s)''',(name,email, hashed_password,gender, dob))
            mysql.connection.commit()
            flash('You have successfully registered!')


        #New User


        # password2 = request.form['password2']
        # confirmPasswordCheck = bcrypt.check_password_hash(hashed_password, password2)



        # print("Password1: ", password1)
        # print("Password2: " , password2)
        # print("Confirm ", confirmPasswordCheck)

        # if(confirmPasswordCheck == 1):
        #     print("yes")
        # print(name)
        # print(email)
        # print(password2 )
        # print(type(password2))
        cursor.close()


    return render_template('register.html', name = "register")
