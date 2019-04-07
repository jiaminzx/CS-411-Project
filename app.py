from flask import Flask, render_template, json, jsonify, request
#import MySQL
import mysql.connector as mariadb

#Use this line for cPanel
# db = mariadb.connect(user='pickles249_admin', password='csProject411!', database='pickles249_test')
# #Use this line for VM
# db = mariadb.connect(user='root', password='password', database='cs411project')
# cursor = db.cursor()


#db.close() needs to be called to close connection


app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi

@app.route("/")
def main():
    return render_template('home.html')


# @app.route("/main")
# def m():
#     return render_template('home.html')


@app.route('/showSignUp')
def signUp():
    return render_template('signup.html')

@app.route('/showModify')
def modify():
    return render_template('modify.html')

@app.route('/showDelete')
def delete():
    return render_template('delete.html')

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
                return "Email already in use"

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
#     app.run(host='sp19-cs411-36.cs.illinois.edu', port=8083)
    app.run(debug = True)
