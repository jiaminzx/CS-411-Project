import re
import mysql.connector as mariadb
import joblib
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

def predictions(array):
    print("loading model")
    model=joblib.load('model.sav')
    print("model loaded")
    proba=model.predict_proba([array])
    print(proba[0][0])

    metric=proba[0][0]
    metric=1-(metric/.843)
    return metric

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
#db = mariadb.connect(user='root', password='password',database='m2z2')

#use this for jiamin's local dev
db = mariadb.connect(user='username', password='password',database='m2z2')

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
        cursor.execute('SELECT * FROM users WHERE userID = "%s"' % (userID))
        rows = cursor.fetchall()
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

        try:

            matches_query = "select YT1.prospecting_id from yeses_tbl as YT1 where YT1.viewed__id = {} and YT1.prospecting_id IN (select YT2.viewed__id from yeses_tbl as YT2 where YT2.prospecting_id = {})".format(userID, userID)
            # matches_view = "CREATE VIEW match_ids AS {}"
            cursor.execute("SELECT * from users WHERE userID IN ({})".format(matches_query))
            print("executed query")
            rows = cursor.fetchall()
            print("got rows")
        except mysql.connector.Error as error:
            print("Failed to get record from database: {}".format(error))

        return render_template('matches.html', data=rows,name=name)

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

    metric=0

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

                
                matchn= rows[userNum][0]
                print(str(matchn)+"in get straight f")
                cursor.execute("SELECT age, ethnicity, job, income FROM users WHERE userID = %s", [str(userID)])
                rows1=cursor.fetchall()

                cursor.execute("SELECT age, ethnicity FROM users WHERE userID = %s", [str(matchn)])
                rows=cursor.fetchall()

                age=rows1[0][0]
                race=rows1[0][1]
                race=re.sub(r'[^\w\s]','',str(race))
                job=rows1[0][2]
                inc=rows1[0][3]
                race=race.lower()
                age2=rows[0][0]
                race2=rows[0][1]
                race2=re.sub(r'[^\w\s]','',str(race2))
                race2=race2.lower()
                if inc==None:
                    inc=-1
                if age2==None:
                    age2=18
                if race2!=race2:
                    race2=6
                if race!=race:
                    race=6
                if job==None:
                    job=18
                if age!=age:
                    age=18
                
                # races={}
                # races[1]='Black'
                # races[2]='White'
                # races[3]='Latino'
                # races[4]='Asian'
                # races[5]='Native American'
                # races[6]='Other'

                if race[0]=='b':
                    race=1
                elif race[0]=='w':
                    race=2
                elif race[0]=='l' or race[0]=='h':
                    race=3
                elif race[0]=='a' or race[0]=='e':
                    race=4
                elif race[0]=='n':
                    race=5
                else:
                    race=6

                if race2[0]=='b':
                    race2=1
                elif race2[0]=='w':
                    race2=2
                elif race2[0]=='l' or race2[0]=='h':
                    race2=3
                elif race2[0]=='a' or race2[0]=='e':
                    race2=4
                elif race2[0]=='n':
                    race2=5
                else:
                    race2=6


                print(age)
                print(race)
                print(job)
                print(inc)
                print(age2)
                print(race2)

                array=[age,race,job,inc,age2,race2]
                #install joblib on pip 

                metric=predictions(array)


            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))

        elif pref=='straight' and gender.lower()=='m':
            genderPref='Women'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'F'")
                rows=cursor.fetchall()

                #insert

            except mysql.connector.Error as error:
                print("Failed to get record from database: {}".format(error))

        return render_template('possibleMatch.html', data=rows,name=name,i=userNum,metric=metric)

    if request.method == 'POST':
        rows=[]
        cursor = db.cursor()

        pref, gender = getPrefandGen(userID, cursor)

        if pref=='straight' and gender.lower()=='f':
            genderPref='Men'
            try:
                cursor.execute("SELECT * FROM users WHERE sex = 'M'")
                rows=cursor.fetchall()

                #insert

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

                #insert

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
@app.route("/message", methods = ["POST", "GET"])
@login_required
def messaging():
    if request.method == 'GET':
        print('Get')

    if request.method == 'POST':
        print('Post')
        recipient = request.form["recipient"]
        print('Want to message ', recipient)

    return redirect(url_for('showMatches'))

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
    #app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
    app.run()
