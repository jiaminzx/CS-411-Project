from flask import Flask, render_template, json, jsonify, request
#import MySQL
import mysql.connector as mariadb

db = mariadb.connect(user='pickles249_admin', password='csProject411!', database='pickles249_test')
cursor = db.cursor()


#db.close() needs to be called to close connection


app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/main")
def m():
    return render_template('index.html')

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


@app.route('/showSignUp')
def signUp():
    return render_template('index2.html')

@app.route('/showSignUp/handle_data', methods=['POST'])
def handle_data():
    # print "HEEEEEEERE"
    if request.method == 'POST':
        projectpath = request.form['projectFilepath']
        #print projectpath

    return render_template('index2.html')


# @app.route('/addU')
@app.route('/showSignUp/adduser', methods=['POST'])
def adduser():
    # print "Entered"
    if request.method == 'POST':
        try:
            name = request.form['inputName']
            password = request.form['inputPassword']
            #CHANGE TO MATCH DATABASE
            cursor.execute("INSERT INTO users (name, email) VALUES (%s,%s)",(name, password))
            db.commit()
            # print "Registered"
        except Exception as e:
          return(str(e))
    return render_template('index2.html')

# #comment out when hosting on cpanel
#COMMENT WHEN HOSTING ON CPANEL
if __name__ == "__main__":
    app.run()
