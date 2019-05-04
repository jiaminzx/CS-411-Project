<<<<<<< HEAD
<<<<<<< HEAD
from flask import Flask, render_template, json,jsonify, request
#import MySQL
import mysql.connector as mariadb



app = Flask(__name__)
application = app


@app.route("/")
def main():
    return render_template('signup.html')

@app.route("/showUsers")
def showUsers():
    mariadb_connection = mariadb.connect(user='username', password='password', database='cs411project')
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    return jsonify(rows)
    mariadb_connection.close()


if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
=======
from flask import Flask, render_template, json, jsonify, request
=======


from flask import Flask, render_template, json, jsonify, request
from flask import flash, redirect, session, abort
import re
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
#import MySQL
import mysql.connector as mariadb

#Use this line for cPanel
db = mariadb.connect(user='pickles249_admin', password='csProject411!', database='pickles249_test')
<<<<<<< HEAD
# #Use this line for VM
# db = mariadb.connect(user='root', password='password', database='cs411project')
cursor = db.cursor()


#db.close() needs to be called to close connection


=======
#Use this line for VM
# db = mariadb.connect(user='root', password='password', database='m2z2')
# cursor = db.cursor(cursor_class=MySQLCursorPrepared)

cursor = db.cursor()

#db.close() needs to be called to close connection

>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi

@app.route("/")
def main():
    return render_template('home.html')

<<<<<<< HEAD

@app.route("/main")
def m():
    return render_template('home.html')

@app.route("/showUsers")
def showUsers():
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    output = jsonify(rows)
    #print rows

    return output


=======
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
@app.route('/showSignUp')
def signUp():
    return render_template('signup.html')

<<<<<<< HEAD
@app.route('/showModify')
def modify():
    return render_template('modify.html')
=======
@app.route('/SignIn')
def modify():
    return render_template('signup.html')
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b

@app.route('/showDelete')
def delete():
    return render_template('delete.html')

@app.route('/showSignUp/handle_data', methods=['POST'])
def handle_data():
    # print "HEEEEEEERE"
    if request.method == 'POST':
        projectpath = request.form['projectFilepath']
<<<<<<< HEAD
        #print projectpath

    return render_template('signup.html')


# @app.route('/addU')
=======

@app.route("/userHome",methods=['GET'])
def userHome():
    userID=int(1)
    genderPref='M'
    if request.method == 'GET':
        rows=[]
        spq = """SELECT orientation FROM users WHERE userID="%d"""
        pref=cursor.execute(spq, (userID))
        print(pref)
        gender=cursor.execute('SELECT sex FROM users WHERE userID="%d"' % (userID))
        print(gender)
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

    return render_template('userHome.html', data=rows, genderPreference=genderPref)


>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
@app.route('/showSignUp', methods=['POST'])
def adduser():
    #print "adduser Entered"
    if request.method == 'POST':
        try:
<<<<<<< HEAD
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']

=======
            #required: name, password, email, height, sex, education, ethnicity
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            height =  request.form['inputHeight']
            sex = request.form['inputGender']
            age = request.form['inputAge']
            cursor.execute('SELECT * FROM users WHERE age="%s"' % (age))
            rows=cursor.fetchall()
            if len(rows) != 0:
                return "You must be above 18"
            education = request.form['inputEducation']
            ethnicity = request.form['inputEthnicity']
            orientation = request.form['orientation']
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
            cursor.execute('SELECT * FROM users WHERE email="%s"' % (email))
            rows=cursor.fetchall()
            if len(rows) != 0:
                #print "Email already in use"
                return "Email already in use"

<<<<<<< HEAD
            cursor.execute("INSERT LOW_PRIORITY INTO users (name, email, password) VALUES (%s,%s, %s)",(username, email, password))
=======
            cursor.execute("INSERT LOW_PRIORITY INTO users (name, email, password, height, sex, age, education, ethnicity,orientation)"
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username, email, password, height, sex, age, education, ethnicity,orientation))
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
            db.commit()
            # print "Registered"
        except Exception as e:
          return(str(e))
    return render_template('signup.html')

<<<<<<< HEAD
=======
@app.route('/showSignIn')
def signIn():
    return render_template('signIn.html')

@app.route('/get_profile', methods = ['POST'])
def get_profile():
    if request.method == 'POST':
        try:
            password = request.form["inputPassword"]
            email = request.form["inputEmail"]
            cursor.execute('SELECT * FROM users WHERE email="%s"' % (email))
            row=cursor.fetchall()
            assert len(row) == 1, "Multiple profiles with same email"
        except Exception as e:
          return(str(e))

    return render_template('get_profile.html', data = row)

>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
@app.route('/showModify', methods=['POST'])
def moduser():
    #print "Entered modUser"
    if request.method == 'POST':
        try:
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
<<<<<<< HEAD

            try:
                cursor.execute('UPDATE LOW_PRIORITY users SET name="%s" WHERE email="%s"' % (username, email))
=======
            height =  request.form['inputHeight']
            sex = request.form['inputGender']
            try:
                cursor.execute('UPDATE LOW_PRIORITY users SET name="%s", height="%s",sex="%s" WHERE email="%s"' % (username, height, sex, email))
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
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


<<<<<<< HEAD
# #comment out when hosting on cpanel
# if __name__ == "__main__":
#     app.run(host='sp19-cs411-36.cs.illinois.edu', port=8083)
>>>>>>> pratheek
=======

# #comment out when hosting on cpanel
# if __name__ == "__main__":
    # app.run(host='sp19-cs411-36.cs.illinois.edu', port=8083)
    # app.run()
>>>>>>> 791cb02666c7ec805d5c09e3ecd910dfd87e020b
