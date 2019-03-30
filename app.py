from flask import Flask, render_template, json,jsonify, request
#from flaskext.mysql import MySQL

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
    mariadb_connection = mariadb.connect(user='pickles249_admin', password='Aelius999!', database='pickles249_test')
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()
    
    return jsonify(rows)
    # return render_template("showUser.html",rows=rows)
    mariadb_connection.close()
    

@app.route('/showSignUp')
def signUp():
    return render_template('index2.html')
   



###remove below if hosting on cpanel
#if __name__ == "__main__":
    #app.run(debug=True)
  #  app.run(host='sp19-cs411-36.cs.illinois.edu', port=5000)
