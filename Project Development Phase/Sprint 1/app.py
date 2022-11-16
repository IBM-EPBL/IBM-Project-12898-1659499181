from flask import Flask, request, redirect, flash, url_for, session
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from threading import Thread
import ibm_db


mailID = "varun10test@gmail.com"
mailIDpass = "123thisisit"

app = Flask(__name__)
app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = '125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud'
app.config['MYSQL_USER'] = '2116190701229@smartinternz.com'
app.config['MYSQL_PASSWORD'] = 'Thuhin@6119'
app.config['MYSQL_DB'] = 'bludb'

#Sending Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = mailID
app.config['MAIL_PASSWORD'] = mailIDpass
mail = Mail(app)

 
mysql = MySQL(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        
        cursor = ibm_db.connection("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt")
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



@app.route('/forgotPass' , methods = ['GET' , 'POST'])
def forgotPass():

    if request.method == 'post':
        email = request.form('email')
        cursor = mysql.connection.cursor()


        #Check for existing user
        cursor.execute('''SELECT * FROM user WHERE email = %s''', [email])
        account = cursor.fetchone()

        if(account):
            msg = Message()
            msg.subject = "Password Reset"
            msg.recipients = email
            msg.sender = mailID
            # msg.html = render_template('reset_email.html', user=account, token=token)



    return render_template('forgotPassword.html')





