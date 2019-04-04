from flask import Flask, render_template, json,jsonify, request
#import MySQL
import mysql.connector as mariadb

db = mariadb.connect(user='root', password='password', database='cs411project')
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
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    return jsonify(rows)


@app.route('/showSignUp')
def signUp():
    return render_template('index2.html')

@app.route('/showSignUp/handle_data', methods=['POST'])
def handle_data():
    # print "HEEEEEEERE"
    if request.method == 'POST':
        projectpath = request.form['projectFilepath']
        print projectpath

    return render_template('index2.html')

    return
# @app.route('/addU')
@app.route('/showSignUp/adduser', methods=['POST'])
def adduser():
    # print "Entered"
    if request.method == 'POST':
        try:
            name = request.form['inputName']
            password = request.form['inputPassword']
            print name, password
            cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)",(name, password))
            db.commit()
            # print "Registered"
        except Exception as e:
           return(str(e))
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
