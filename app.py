
from flask import Flask, render_template, json, jsonify, request
from flask import flash, redirect, session, abort,url_for, make_response
from flask_login import LoginManager , login_required , UserMixin , login_user
import re
#import MySQL
import mysql.connector as mariadb

#Use this line for cPanel
db = mariadb.connect(user='root', password='password', database='m2z2')
#Use this line for VM
# db = mariadb.connect(user='user', password='password',database='m2z2')
cursor = db.cursor(buffered= True)

#db.close() needs to be called to close connection
app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username , key='secret_key')

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.id = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def remove_user(self,userID):
        self.users_id_dict.pop(userID)

users_repository = UsersRepository()


@app.route("/")
def main():
    return render_template('home.html')

@app.route('/showSignUp')
def signUp():
    return render_template('signup.html')

@app.route('/SignIn' , methods=['GET', 'POST'])
def login():
    error=''
    if request.method == 'POST':
        try:
            cursor = db.cursor(buffered= True)
            username = request.form['inputName']
            password = request.form['inputPassword']
            spq = """SELECT userID FROM users WHERE name = %s AND password=%s"""
            cursor.execute(spq, [str(username),str(password)])
            userID=cursor.fetchall()

            print(userID)
            userID=re.sub(r'[^\w\s]','',str(userID))

            # print(userID)
            new_user = User(username , password , userID)
            users_repository.save_user(new_user)

            registeredUser = users_repository.get_user(username)
            # print('Users '+ str(users_repository.users))
            # print('Register user %s , password %s' % (registeredUser.username, registeredUser.password))
            if not userID:
                error="invalid username or pass"

                # return redirect(url_for('userHome'))
            else:
                print('Logged in..')
                #registeredUser=str(registeredUser)
                #session['user'] = userID
                resp = redirect(url_for("userHome"))
                resp.set_cookie('Login',registeredUser.id)
                login_user(registeredUser)
                return resp
        except Exception as e:
            return(str(e))
    return render_template('signIn.html',error=error)

@app.route("/userHome",methods=['GET','POST'])
@login_required
def userHome():

    userID = request.cookies.get('Login')
    print("user in session:" +str(userID))

    # CREATE VIEW `view_name` AS SELECT statement

    registeredUser = users_repository.get_user_by_id(userID)
    name=registeredUser.username
    print(name)
    if request.method == 'GET':
        rows=[]
        cursor = db.cursor()

        #use of prepared statment
        spq = """SELECT orientation FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        pref=cursor.fetchall()
        pref=re.sub(r'[^\w\s]','',str(pref))
        pref=pref[1:]

        spq="""SELECT sex FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        gender=cursor.fetchall()
        gender=re.sub(r'[^\w\s]','',str(gender))
        gender=gender[1:]

        if pref=='straight' and gender.lower()=='f':
            genderPref='Men'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'M'")
                rows=cursor.fetchall()
            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))

        elif pref=='straight' and gender.lower()=='m':
            genderPref='Women'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'F'")
                rows=cursor.fetchall()
            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))
        return render_template('userHome.html', data=rows,name=name)

    return render_template('userHome.html',name=name)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('Login', None)
    return redirect(url_for('main'))

@app.route('/showDelete')
def delete():
    return render_template('delete.html')

@app.route('/showSignUp/handle_data', methods=['POST'])
def handle_data():
    # print "HEEEEEEERE"
    if request.method == 'POST':
        projectpath = request.form['projectFilepath']


@app.route('/showSignUp', methods=['POST'])
def adduser():
    #print "adduser Entered"
    if request.method == 'POST':
        try:
            #required: name, password, email, height, sex, education, ethnicity
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            height = request.form['inputHeight']
            sex = request.form['inputGender']
            age = request.form['inputAge']
            education = request.form['inputEducation']
            ethnicity = request.form['inputEthnicity']
            orientation = request.form['orientation']

            if age<18:
                return "You must be above 18"

            cursor.execute('SELECT * FROM users WHERE email="%s"' % (email))
            rows=cursor.fetchall()
            if len(rows) != 0:
                return "Email already in use"

            cursor.execute("INSERT LOW_PRIORITY INTO users (name, email, password, height, sex, age, education, ethnicity,orientation)"
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username, email, password, height, sex, age, education, ethnicity,orientation))
            db.commit()
            # print "Registered"
        except Exception as e:
          return(str(e))
    return render_template('signup.html')

@app.route('/showModify', methods=['POST'])
def moduser():
    #print "Entered modUser"
    if request.method == 'POST':
        try:
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            height =  request.form['inputHeight']
            sex = request.form['inputGender']
            try:
                cursor.execute('UPDATE LOW_PRIORITY users SET name="%s", height="%s",sex="%s" WHERE email="%s"' % (username, height, sex, email))
                db.commit()
            except Exception as e:
              return(str(e))
            # cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s, %s)",(username, email, password))
            # db.commit()

        except Exception as e:
          return(str(e))
    return render_template('modify.html')

@app.route('/showDelete', methods=['POST'])
def deluser():
    #print "Entered delUser"
    if request.method == 'POST':
        try:
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            try:
                cursor.execute('DELETE FROM users WHERE name="%s" and email="%s" and password="%s"' % (username, email, password))
                db.commit()
            except Exception as e:
              return(str(e))
            # print "Registered"
        except Exception as e:
          return(str(e))
    return render_template('delete.html')

userNum = -1
@app.route("/swipe", methods = ["POST", "GET"])
@login_required
def show_user_queue():
    n_profiles_to_fetch = 2
    global userNum
    userNum = userNum + 1

    userID = request.cookies.get('Login')
    print("user in session:" +str(userID))

    # CREATE VIEW `view_name` AS SELECT statement

    registeredUser = users_repository.get_user_by_id(userID)
    name=registeredUser.username
    print(name)
    if request.method == 'GET':
        rows=[]
        cursor = db.cursor()

        #use of prepared statment
        spq = """SELECT orientation FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        pref=cursor.fetchall()
        pref=re.sub(r'[^\w\s]','',str(pref))
        pref=pref[1:]

        spq="""SELECT sex FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        gender=cursor.fetchall()
        gender=re.sub(r'[^\w\s]','',str(gender))
        gender=gender[1:]

        if pref=='straight' and gender.lower()=='f':
            genderPref='Men'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'M'")
                rows=cursor.fetchall()
            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))

        elif pref=='straight' and gender.lower()=='m':
            genderPref='Women'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'F'")
                rows=cursor.fetchall()
            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))
        return render_template('possibleMatch.html', data=rows,name=name,i=userNum)

    if request.method == 'POST':
        rows=[]
        cursor = db.cursor()

        #use of prepared statment
        spq = """SELECT orientation FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        pref=cursor.fetchall()
        pref=re.sub(r'[^\w\s]','',str(pref))
        pref=pref[1:]

        spq="""SELECT sex FROM users WHERE userID= %s"""
        cursor.execute(spq, [str(userID)])
        gender=cursor.fetchall()
        gender=re.sub(r'[^\w\s]','',str(gender))
        gender=gender[1:]

        if pref=='straight' and gender.lower()=='f':
            genderPref='Men'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'M'")
                rows=cursor.fetchall()

                # insert into yeses_tbl
                # decision = request.form["value"]
                decision = request.data
                # print(decision)
                # if decision == "yes":
                cursor.execute("INSERT INTO yeses_tbl (prospecting_id, viewed__id) VALUES ({},{})".format(str(userID), rows[0]))
            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))

        elif pref=='straight' and gender.lower()=='m':
            genderPref='Women'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'F'")
                rows=cursor.fetchall()

                # insert into yeses_tbl
                # decision = request.form["value"]
                decision = request.data
                print("able to access value in form")
                # if decision == "yes":
                cursor.execute("INSERT INTO yeses_tbl (prospecting_id, viewed__id) VALUES ({},{})".format(str(userID), rows[0]))
            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))
        return render_template('possibleMatch.html', data=rows,name=name,i=userNum)

    # return render_template('possibleMatch.html',name=name)

# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return flask.Response('<p>Login failed</p>')

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)

# #comment out when hosting on cpanel
if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8084)
    app.run()
