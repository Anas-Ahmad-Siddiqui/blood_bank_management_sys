from flask import Flask, render_template, request, redirect, url_for, session
import re
import os
import sys
import cx_Oracle

if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/instantclient_19_3")
elif sys.platform.startswith("win32"):
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\instantclient_19_11")
    

dsn_tns = cx_Oracle.makedsn(r'Acer-Aspire-7', '1521', service_name='XE') 
con = cx_Oracle.connect(user=r'blood_bank', password='12345', dsn=dsn_tns) 

cursor = con.cursor()

for row in cursor.execute("SELECT * FROM login where login_username='anas' and login_password='anas_hokage'"):
    print(row)


app = Flask(__name__)

@app.route('/')

def hello():
    return render_template('index.html')

@app.route('/form_login', methods=['GET', 'POST'])

def login():
    # Output message if something goes wrong...
    msg = ''
    username = request.form.get('username-123')
    password = request.form.get('password-123')

    print(username,'\n', password)

    cursor = con.cursor()

    cursor.execute("SELECT * FROM login WHERE LOGIN_USERNAME = :s AND LOGIN_PASSWORD = :s",[username,password])

    account = cursor.fetchone()

    if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            msg = 'Logged in successfully!'

            return redirect(url_for('selection'))
           
    else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


@app.route('/selection')

def selection():
    return render_template('selection.html')




@app.route('/insert_user')
def insert_user():
    return render_template('insert-user-data.html')


@app.route('/insert_user_data', methods=['GET', 'POST'])
def insert_user_data():
 
    user_id = request.form.get('user-id')
    f_name = request.form.get('f_name')
    l_name = request.form.get('l_name')
    mobile = request.form.get('Mobile')
    e_mail = request.form.get('e_mail')

    cursor = con.cursor()

    cursor.execute("INSERT INTO USER_ VALUES ( :a ,  :b ,  :c , :d ,  :e )",a=user_id, b=f_name, c=l_name, d=mobile, e=e_mail)
    cursor.execute("commit")
    
    return render_template('insert-user-data.html')

@app.route('/insert_bbank')
def insert_bbank():
    return render_template('Insert-Blood-Bank-data.html')

@app.route('/insert_bbank_data', methods=['GET', 'POST'])
def bbank_data():

    no = request.form.get('b_no')
    name = request.form.get('name')
    location = request.form.get('location')

    cursor = con.cursor()

    cursor.execute("INSERT INTO blood_bank VALUES(:a, :b, :c)", a=no, b=name, c=location)
    cursor.execute("commit")

    return render_template('insert-blood-bank-data.html')

@app.route('/insert_donor')
def insert_donor():
    return render_template('Insert-Donor-Data.html')

@app.route('/insert_donor_data', methods = ['GET', 'POST'])
def insert_donor_data():

    no = request.form.get('d_no')
    f_name = request.form.get('f_name')
    l_name = request.form.get('l_name')
    mobile = request.form.get('mobile')
    address = request.form.get('address')

    cursor.execute("INSERT INTO donor VALUES( :a , :b , :c , :d , :e , :f )", a = no , b = f_name, c=l_name, d=address, e=mobile, f='24-JUN-21')
    cursor.execute("commit")

    return render_template('Insert-Donor-Data.html')

@app.route('/insert_hospital')
def insert_hospital():
    return render_template('insert-hospital-data.html')

@app.route('/insert_hospital_data', methods = ['GET', 'POST'])
def insert_hospital_data():
    
    id = request.form.get('h_id')
    name = request.form.get('name')
    e_mail = request.form.get('e_mail')
    mobile = request.form.get('mobile')

    cursor = con.cursor()

    cursor.execute("INSERT INTO hospitals VALUES( :a , :b , :c , :d )", a=id, b=name, c=e_mail, d=mobile)
    cursor.execute("commit")

    return render_template('insert-hospital-data.html')


@app.route('/insert_patients')
def insert_patients():
    return render_template('insert-patients-data.html')

@app.route('/insert_patients_data', methods = ['GET', 'POST'])
def insert_patients_data():

    id = request.form.get('p_id')
    name = request.form.get('name')
    req = request.form.get('requirement')

    cursor = con.cursor()

    cursor.execute("INSERT INTO patients VALUES( :a , :b , :c )", a=id, b=name, c=req)
    cursor.execute("commit")

    return render_template('insert-patients-data.html')


@app.route('/insert_user_id')
def insert_user_id():
    return render_template('insert-login-info.html')

@app.route('/insert_user_id_data', methods = ['GET', 'POST'])
def insert_user_id_data():

    id = request.form.get('id')
    username = request.form.get('username')
    password = request.form.get('password')

    cursor = con.cursor()

    cursor.execute("INSERT INTO login VALUES( :a , :b , :c)", a=id, b=username, c=password)
    cursor.execute("commit")

    return render_template('insert-login-info.html')


    


app.secret_key = 'super secret key'
app.run(debug=True)
