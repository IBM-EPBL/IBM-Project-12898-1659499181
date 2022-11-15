from flask import Flask, request, redirect, flash, url_for, session
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

        cursor.execute('''SELECT * FROM user WHERE email = %s''', [email])
        account = cursor.fetchone()
        password = request.form['password']
        # print(account[2])

        confirmPasswordCheck = bcrypt.check_password_hash(account[2], password)
        if(confirmPasswordCheck):
            session['loggedin'] = True
            session['username'] = account[1]
            return redirect(url_for('home'))
        else:
            print("Hello")
            flash('Incorrect username/password')
    else:
        flash('Incorrect username/password')

        # return redirect(url_for('home'))


    return render_template('login.html', name = "login")


@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   flash("You have successfully logged out, please log in again!")
   return redirect(url_for('login'))

@app.route('/')
def home():

    if 'loggedin' in session:
        print("Hi")
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


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
            flash('You have successfully registered! Please login')

            return redirect(url_for('login'))

        cursor.close()


    return render_template('register.html', name = "register")
