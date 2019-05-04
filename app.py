

from flask import Flask, render_template, json, jsonify, request, abort, redirect, Response, url_for, flash

# from flask.ext.login import LoginManager
from flask_login import LoginManager, login_required , UserMixin , login_user
#import MySQL
import mysql.connector as mariadb

#Use this line for cPanel
# db = mariadb.connect(user='pickles249_admin', password='csProject411!', database='pickles249_test')
#Use this line for VM
db = mariadb.connect(user='root', password='password', database='cs411project')
cursor = db.cursor()
#db.close() needs to be called to close connection

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
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier +=1
        return self.identifier

users_repository = UsersRepository()

app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi
app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

@app.route("/")
def main():
    return render_template('home.html')


@app.route('/showSignUp')
def signUp():
    return render_template('signup.html')

@app.route('/showModify')
def modify():
    return render_template('modify.html')

@app.route('/showDelete')
def delete():
    return render_template('delete.html')

@app.route('/showMessage')
def messages():
    return render_template('messages.html')

@app.route('/showSignUp/handle_data', methods=['POST'])
def handle_data():
    # print "HEEEEEEERE"
    if request.method == 'POST':
        projectpath = request.form['projectFilepath']
        #print projectpath

    # return render_template('signup.html')


# @app.route('/addU')
@app.route('/showSignUp', methods=['POST'])
def adduser():
    #print "adduser Entered"
    if request.method == 'POST':
        try:
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            height =  request.form['inputHeight']
            sex = request.form['inputGender']
            cursor.execute('SELECT * FROM users WHERE email="%s"' % (email))
            rows=cursor.fetchall()
            if len(rows) != 0:
                #print "Email already in use"
                flash('Email already in use. Sign up with a different email')
                return render_template('signup.html')

            cursor.execute("INSERT LOW_PRIORITY INTO users (name, email, password, height, sex) VALUES (%s,%s, %s, %s, %s)",(username, email, password, height, sex))
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

@app.route("/showSignIn",methods=['POST'])
def showSignIn():


    if request.method == 'POST':
        try:
            email = request.form['inputEmail']
            password = request.form['inputPassword']
            cursor.execute("SELECT * FROM users WHERE sex = 'M'")
            rows=cursor.fetchall()
        except Exception as e:
          return(str(e))

    return render_template('showSignIn.html')

@app.route("/showUsers")
def showUsers():
    return render_template('showUser.html')

@app.route("/showMen",methods=['GET'])
def showMen():
    if request.method == 'GET':
        try:
            #CHANGE QUERY TO MATCH DATABASE
            cursor.execute("SELECT * FROM users WHERE sex = 'M'")
            rows=cursor.fetchall()
        except Exception as e:
          return(str(e))

    return render_template('showMen.html', data=rows)

@app.route("/showWomen",methods=['GET'])
def showWomen():
    if request.method == 'GET':
        try:
            #CHANGE QUERE TO MATCH DATABASE
            cursor.execute("SELECT * FROM users WHERE sex = 'F'")
            rows=cursor.fetchall()
        except Exception as e:
          return(str(e))

    return render_template('showWomen.html', data=rows)

# #comment out when hosting on cpanel
if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8082)
    # app.run()
