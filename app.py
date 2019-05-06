import re
import mysql.connector as mariadb
from flask import Flask, render_template, json, jsonify, request
from flask import flash, redirect, session, abort,url_for, make_response
from flask_login import LoginManager , login_required , UserMixin , login_user

# cursor.execute(" drop trigger if exists mytrigger")
# qrystr = "CREATE TRIGGER HeightReset BEFORE UPDATE ON users FOR EACH ROW BEGIN IF NEW.height < 0 OR NEW.height > 108 THEN SET NEW.height = OLD.height; END IF; END"
# cursor.execute(qrystr)
# db.commit()

class User(UserMixin):
    def __init__(self , email , password , id , active=True):
        self.id = id
        self.email = email
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.email , key='secret_key')

class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.id = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)

        self.users.setdefault(user.email, user)

    def get_user(self, email):
        return self.users.get(email)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def remove_user(self,userID):
        self.users_id_dict.pop(userID)

def getName(registeredUser, cursor):
        cursor.execute('SELECT name FROM users WHERE email="%s"' % (registeredUser.email))
        names=cursor.fetchall() #should only retrieve one value
        names=re.sub(r'[^\w\s]','',str(names))
        name=names[1:]
        return name

def getPrefandGen(userID, cursor):
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

        return pref, gender

#Use this line for cPanel
# db = mariadb.connect(user='root', password='password', database='m2z2')
#Use this line for VM
db = mariadb.connect(user='root', password='password',database='m2z2')
# db = mariadb.connect(user='user', password='password',database='m2z2')

cursor = db.cursor(buffered= True)

#db.close() needs to be called to close connection
app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

users_repository = UsersRepository()


@app.route("/")
def main():
    return render_template('home.html')

@app.route('/showSignUp')
def signUp():
    return render_template('signup.html')

@app.route('/showDelete')
def delete():
    return render_template('delete.html')

@app.route('/showModify')
def modify():
    return render_template('modify.html')

@app.route('/SignIn' , methods=['GET', 'POST'])
def login():
    error=''
    if request.method == 'POST':
        try:
            cursor = db.cursor(buffered= True)
            email = request.form['inputEmail']
            password = request.form['inputPassword']
            spq = """SELECT userID FROM users WHERE email = %s AND password=%s"""
            cursor.execute(spq, [str(email),str(password)])
            userID=cursor.fetchall()

            print(userID)
            userID=re.sub(r'[^\w\s]','',str(userID))

            new_user = User(email , password , userID)
            users_repository.save_user(new_user)

            registeredUser = users_repository.get_user(email)
            if not userID:
                error="invalid email or password"
            else:
                print('Logged in..')
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
    cursor = db.cursor()
    name = getName(registeredUser, cursor)
    rows=[]
    print(name)
    if request.method == 'GET':
        pref, gender = getPrefandGen(userID, cursor)

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
    # remove the email from the session if it's there
    session.pop('Login', None)
    return redirect(url_for('main'))

@app.route('/showSignUp', methods=['POST'])
def adduser():
    error=''
    if request.method == 'POST':
        try:
            #required: name, password, email, height, sex, education, ethnicity
            name = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            height = request.form['inputHeight']
            sex = request.form['inputGender']
            age = request.form['inputAge']
            education = request.form['inputEducation']
            ethnicity = request.form['inputEthnicity']
            orientation = request.form['orientation']
            print(age)

            if (int(age) < 18):
                print("Error")
                error="You must be above 18"
            elif( int(height) < 0 or int(height) > 108):
                print("Error")
                error="Your height doesn't fit the range"
            else:
                cursor.execute('SELECT * FROM users WHERE email="%s"' % (email))
                duplicate_emails=cursor.fetchall()
                if len(duplicate_emails) != 0:
                    error="Email already in use"
                else:
                    cursor.execute("INSERT LOW_PRIORITY INTO users (name, email, password, height, sex, age, education, ethnicity,orientation)"
                                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name, email, password, height, sex, age, education, ethnicity,orientation))
                    db.commit()

        except Exception as e:
          return(str(e))
    return render_template('signup.html', error=error)

@app.route('/showModify', methods=['POST'])
def moduser():
    error=''
    userID = request.cookies.get('Login')
    print("user in session:" +str(userID))
    registeredUser = users_repository.get_user_by_id(userID)
    if request.method == 'POST':
        try:
            print("Reached")
            email = registeredUser.email
            cursor.execute('SELECT * FROM users WHERE email="%s"' % (email))
            user_info=cursor.fetchall()
            print("Reached!")
            name = request.form['inputName']
            password = request.form['inputPassword']
            height = request.form['inputHeight']
            sex = request.form['inputGender']
            age = request.form['inputAge']
            education = request.form['inputEducation']
            ethnicity = request.form['inputEthnicity']
            orientation = request.form['orientation']
            print(name, email, password, height, sex, age, education, ethnicity,orientation)
            for value in user_info:
                if(name == u''):
                    name = value[18]
                if(password == u''):
                    password = value[17]
                if(height == u''):
                    height = value[7]
                if(sex == u'no change'):
                    sex = value[15]
                if(age == u''):
                    age = value[1]
                if(education == u''):
                    education = value[5]
                if(ethnicity ==  u'no change'):
                    ethnicity = value[6]
                if(orientation ==  u'no change'):
                    orientation = value[12]
            print("Reached!!")
            print(name, email, password, height, sex, age, education, ethnicity,orientation)
            if int(age)<18:
                return render_template('modify.html', error="Cannot change heigt to go below 18")

            print(name, email, password, height, sex, age, education, ethnicity,orientation)
            cursor.execute('UPDATE LOW_PRIORITY users SET name="%s", password="%s", height="%s", sex="%s", age="%s", education="%s", ethnicity="%s", orientation="%s" WHERE email="%s"' \
             % (name, password, height, sex, age, education, ethnicity, orientation, email))

            # cursor.execute('UPDATE LOW_PRIORITY users SET name="%s", height="%s",sex="%s" WHERE email="%s"' % (username, height, sex, email))
            db.commit()
            flash("Updated")
            print("Reached!!!")
        except Exception as e:
          return(str(e))
    return render_template('modify.html', error=error)

@app.route('/showDelete', methods=['POST'])
def deluser():
    print("Time to delete")
    userID = request.cookies.get('Login')
    print("user in session:" +str(userID))

    registeredUser = users_repository.get_user_by_id(userID)
    try:
        #will need to add deletes to all other tables too
        cursor.execute('DELETE FROM users WHERE email="%s"' % (registeredUser.email))
        db.commit()
    except Exception as e:
      return(str(e))

    #Same as logout
    session.pop('Login', None)
    return redirect(url_for('main'))

@app.route("/showMatches", methods = ['GET'])
def showMatches():
    userID = request.cookies.get('Login')
    print("user in session:" +str(userID))

    # CREATE VIEW `view_name` AS SELECT statement

    registeredUser = users_repository.get_user_by_id(userID)
    cursor = db.cursor()
    name = getName(registeredUser, cursor)
    rows=[]
    print(name)
    if request.method == 'GET':
        pref, gender = getPrefandGen(userID, cursor)

        # if pref=='straight' and gender.lower()=='f':
        #     genderPref='Men'
        try:
            # "select YT1.prospecting_id from yeses_tbl as YT1 where YT1.viewed__id = 6 and  YT1.prospecting_id IN (select YT2.viewed__id from yeses_tbl as YT2 where YT2.prospecting_id = 6);"
            # "SELECT DISTINCT ptsoy FROM (SELECT prospecting_id AS ptsoy FROM yeses_tbl as yeses1 WHERE viewed__id = 6) AS matches_ids WHERE ptsoy IN (SELECT viewed__id AS pyso FROM yeses_tbl as yeses2 WHERE prospecting_id = 6)"
            # ptsoy_query = "SELECT prospecting_id as ptsoy_id FROM yeses_tbl as yeses1 WHERE viewed__id = {}".format(userID)
            # ptsoy_view = "CREATE VIEW ptsoy AS {}".format(ptsoy_query)
            # cursor.execute(ptsoy_view)

            # pyso_query = "SELECT viewed__id AS pyso_id FROM yeses_tbl as yeses2 WHERE prospecting_id = {}".format(userID)
            # pyso_view = "CREATE VIEW pyso AS {}".format(pyso_query)
            # cursor.execute(pyso_view)
            # matches_query = "{} INTERSECT {}".format(ptsoy_query, pyso_query)
            # ptsoy_pyso_intersect = "SELECT DISTINCT ptsoy_id FROM ptsoy AS matches_ids WHERE ptsoy_id IN pyso.pyso_id"

            # matches_view_stmt = "CREATE VIEW matches AS {}".format(ptsoy_pyso_intersect)
            # cursor.execute(matches_view_stmt)
            # cursor.execute("SELECT * FROM users AS match_profiles WHERE userID IN (SELECT * FROM matches)")
            # rows=cursor.fetchall()

            matches_query = "select YT1.prospecting_id from yeses_tbl as YT1 where YT1.viewed__id = {} and YT1.prospecting_id IN (select YT2.viewed__id from yeses_tbl as YT2 where YT2.prospecting_id = {})".format(userID, userID)
            # matches_view = "CREATE VIEW match_ids AS {}"
            cursor.execute("SELECT * from users WHERE userID IN ({})".format(matches_query))
            print("executed query")
            rows = cursor.fetchall()
            print("got rows")
        except mysql.connector.Error as error:
            print("Failed to get record from database: {}".format(error))

    # elif pref=='straight' and gender.lower()=='m':
    #     genderPref='Women'
    #     try:
    #         # ptsoy_query = "SELECT prospecting_id FROM yeses_tbl WHERE viewed__id = {}".format(userID)
    #         # pyso_query = "SELECT viewed__id FROM yeses_tbl WHERE prospecting_id = {}".format(userID)
    #         # matches_query = "{} INTERSECT {}".format(ptsoy_query, pyso_query)
    #         # matches_view_stmt = "CREATE VIEW matches AS {}".format(matches_query)
    #         # cursor.execute(matches_view_stmt)
    #         # cursor.execute("SELECT * FROM matches")
    #         # rows=cursor.fetchall()
    #         matches_query = "select YT1.prospecting_id from yeses_tbl as YT1 where YT1.viewed__id = {} and YT1.prospecting_id IN (select YT2.viewed__id from yeses_tbl as YT2 where YT2.prospecting_id = {})".format(userID, userID)
    #         # matches_view = "CREATE VIEW match_ids AS {}"
    #         cursor.execute("SELECT * from users WHERE userID IN ".format(matches_query))
    #         rows = cursor.fetchall()
    #     except mysql.connector.Error as error:
    #         print("Failed to get record from database: {}".format(error))
        return render_template('userHome.html', data=rows,name=name)

    # return render_template('userHome.html',name=name)

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
    cursor = db.cursor()
    name = getName(registeredUser, cursor)
    rows=[]
    print(name)
    if request.method == 'GET':
        rows=[]
        cursor = db.cursor()

        pref, gender = getPrefandGen(userID, cursor)

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

        pref, gender = getPrefandGen(userID, cursor)

        if pref=='straight' and gender.lower()=='f':
            genderPref='Men'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'M'")
                rows=cursor.fetchall()

                # insert into yeses_tbl
                decision = request.form["decision"]
                # decision = request.data
                print(decision)
                if decision == "yes":
                    cursor.execute("INSERT LOW_PRIORITY INTO yeses_tbl (prospecting_id, viewed__id)"
                                   "VALUES (%s,%s)",(userID, rows[userNum - 1][0]))
                    db.commit()

            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))

        elif pref=='straight' and gender.lower()=='m':
            genderPref='Women'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'F'")
                rows=cursor.fetchall()

                # insert into yeses_tbl
                decision = request.form["decision"]
                print(decision)
                # print("able to access value in form")
                if decision == "yes":
                # quer = "INSERT INTO yeses_tbl (prospecting_id, viewed__id) VALUES ({},{:d})".format(str(userID), rows[userNum - 1][0])
                    cursor.execute("INSERT LOW_PRIORITY INTO yeses_tbl (prospecting_id, viewed__id)"
                                   "VALUES (%s,%s)",(userID, rows[userNum - 1][0]))
                    db.commit()
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
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8040)
    # app.run()
