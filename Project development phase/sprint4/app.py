from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
app = Flask(__name__)


Conn=ibm_db.connect("database=bludb;hostname=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;port=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;uid=brv13326;pwd=c3GnX6SgfSkf3dyS" , '','')

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login1')
def login1():
    return render_template('login.html')
@app.route('/register1')
def register1():
    return render_template('register.html')
@app.route('/about1')
def about1():
    return render_template('about.html')
@app.route('/help1')
def help1():
    return render_template('help.html')
@app.route('/report')
def report():
    return render_template('report.html')

 
@app.route('/login', methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST'and 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']
         stmt = ibm_db.prepare(Conn,'SELECT * FROM users WHERE username = ? AND password = ?')
         ibm_db.bind_param(stmt,1,username)
         ibm_db.bind_param(stmt,2,password) 
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         if account:
             session['loggedin'] = True
             session['username'] = account['USERNAME']
             msg = 'Logged in successfully !'
             return render_template('home2.html', msg = msg)
         else:
             msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
@app.route('/logout')
def logout():
     session.pop('loggedin', None)
     session.pop('id', None)
     session.pop('username', None)
     return redirect(url_for('login'))
@app.route('/register', methods =['GET', 'POST'])
def register():
     msg = ''
     if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']
         phone_no=request.form['no']
         sql = "SELECT * FROM users WHERE username = ? "
         stmt = ibm_db.prepare(Conn,sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
             msg = 'Account already exists !'
         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
             msg = 'Invalid email address !'
         elif not re.match(r'[A-Za-z0-9]+', username):
             msg = 'Username must contain only characters and numbers !'
         elif not username or not password or not email:
             msg = 'Please fill out the form !'
         else:
             insert_sql = "INSERT INTO users VALUES (?, ?, ?,?)"
             stmt = ibm_db.prepare(Conn,insert_sql)
             ibm_db.bind_param(stmt, 1, username)
             ibm_db.bind_param(stmt, 2, email)
             ibm_db.bind_param(stmt, 3, password)
             ibm_db.bind_param(stmt, 4, phone_no)
             ibm_db.execute(stmt)
             msg = 'You have successfully registered !'
     elif request.method == 'POST':
          msg = 'Please fill out the form !'
     
     return render_template('register.html', msg = msg) 
if __name__=='__main__':
    app.run(debug=True)