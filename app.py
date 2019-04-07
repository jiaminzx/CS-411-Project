from flask import Flask, render_template, json, jsonify, request
#import MySQL
import mysql.connector as mariadb

#Use this line for cPanel
#db = mariadb.connect(user='pickles249_admin', password='csProject411!', database='pickles249_test')
##Use this line for VM
db = mariadb.connect(user='root', password='password', database='cs411project')
cursor = db.cursor()


#db.close() needs to be called to close connection


app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi

@app.route("/")
def main():
    return render_template('home.html')


# @app.route("/main")
# def m():
#     return render_template('home.html')

@app.route("/showUsers")
def showUsers():
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    output = jsonify(rows)
    print(output)

    return output


@app.route('/showSignUp')
def signUp():
    return render_template('signup.html')

@app.route('/deletepg')
def delUser():
    return render_template('delusers.html')

# @app.route('/showSignUp/handle_data', methods=['POST'])
# def handle_data():
#     # print "HEEEEEEERE"
#     if request.method == 'POST':
#         projectpath = request.form['projectFilepath']
        #print projectpath

    # return render_template('signup.html')


# @app.route('/addU')
@app.route('/showSignUp/adduser', methods=['POST'])
def adduser():
    # print "Entered"
    if request.method == 'POST':
        try:
            username = request.form['inputName']
            password = request.form['inputPassword']
            email = request.form['inputEmail']
            #print name, password
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s, %s)",(username, email, password))
            db.commit()
            # print "Registered"
        except Exception as e:
          return(str(e))
    return render_template('signup.html')

@app.route('/deletepg/deluser', methods=['POST'],endpoint = 'deluser')
def deluser():
    if request.method == 'POST':
        try:
            email = request.form['inputEmail']
            #print name, password
            cursor.execute("DELETE FROM users WHERE email = %s" % (email))
            db.commit()
            # print "Registered"
        except Exception as e:
          return(str(e))
    return render_template('delusers.html')


# #comment out when hosting on cpanel
if __name__ == "__main__":
	app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
