from flask import Flask, render_template, json,jsonify, request
#import MySQL
import mysql.connector as mariadb



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
    mariadb_connection = mariadb.connect(user='username', password='password', database='cs411project')
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()
    
    return jsonify(rows)
    mariadb_connection.close()
    

if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
