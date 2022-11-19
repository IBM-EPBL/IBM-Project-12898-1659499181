import imp
from flask import Flask, request, redirect, flash, url_for, session, jsonify
from flask import render_template
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from threading import Thread
import ibm_db
from modelExtraction import main
import regex
import joblib

mailID = "varun10test@gmail.com"
mailIDpass = "123thisisit"

app = Flask(__name__)
app.secret_key = "super secret key"

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fgq80014;PWD=FfWqq4xxSBCf7CAO","","")

#Sending Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = mailID
app.config['MAIL_PASSWORD'] = mailIDpass
mail = Mail(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        bcrypt = Bcrypt()      
        sql = f"""SELECT * FROM "FGQ80014"."user" WHERE "email" = '{email}'"""
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        password = request.form['password']
        confirmPasswordCheck = bcrypt.check_password_hash(dictionary[2], password)
        if(confirmPasswordCheck):
            session['loggedin'] = True
            session['username'] = dictionary[1]
            return redirect(url_for('home'))
        else:
            print("Hello")
            flash('Incorrect username/password')
    else:
        flash('Incorrect username/password')
    return render_template('login.html', name = "login")

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   flash("You have successfully logged out, please log in again!")
   return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def home():
    
    
    if request.method == 'POST':
        url = request.form["url"]

        if(not(regex.search(r'^(http|ftp)s?://', url))):
            print("ERRORR")
            flash("Please input full url, for example- https://facebook.com or else it is a phishing site")
            return render_template('home.html')
        print(url)
        val = main(url)
        print(val) #Check this val

        classifier = joblib.load('webPhishingDetectorSVM.pkl')

        prediction = classifier.predict(val)
        print(prediction)

        if prediction[0]==1 :
            flash("This is a legitimate site!")
            print('website is legitimate')
        elif prediction[0]==-1:
            flash('This is a phishing site!')
            print('Phishing site')


        return render_template('home.html')

    else:
        return redirect(url_for('login'))


@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob= request.form['dob']
        gender = "M"
        bcrypt = Bcrypt()
        hashed_password = bcrypt.generate_password_hash(request.form['password1']).decode('utf-8')
        sql = f"""SELECT COUNT(*) FROM "FGQ80014"."user" WHERE "email" = '{email}' """
        
        #Check for existing user
        stmnt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmnt)
        if dictionary:
            flash('Account already exists!')

        else:
            sql2 = f"""INSERT INTO "FGQ80014"."user" VALUES('{name}','{email}', '{hashed_password}','{gender}', '{dob}')"""
            reg_user = ibm_db.exec_immediate(conn, sql2)
            flash('You have successfully registered! Please login')
            return redirect(url_for('login'))

    return render_template('register.html', name = "register")



@app.route('/forgotPass' , methods = ['GET' , 'POST'])
def forgotPass():
    if request.method == 'post':
        email = request.form('email')

        #Check for existing user
        cursor.execute('''SELECT * FROM user WHERE email = %s''', [email])
        account = cursor.fetchone()

        if(account):
            msg = Message()
            msg.subject = "Password Reset"
            msg.recipients = email
            msg.sender = mailID

    return render_template('forgotPassword.html')

# endpoint for extension

@app.route('/extension', methods=['GET','POST'])
def extension():
    print('extension')
    if request.method == 'GET':
        url = request.args.get("url")
        print(url)
        val = main(url)
        print("Val: " , val)
        classifier = joblib.load('webPhishingDetectorSVM.pkl')
        prediction = classifier.predict(val)
        print(prediction)
        return jsonify({'prediction':str(prediction[0])})