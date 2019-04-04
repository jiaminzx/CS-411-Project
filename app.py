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
    return render_template('index2.html')

@app.route("/showUsers")
def showUsers():
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    return jsonify(rows)


@app.route('/showSignUp')
def signUp():
    adduser()
    return render_template('index2.html')
    # try:
    #     _name = request.form['inputName']
    #     _email = request.form['inputEmail']
    #     _password = request.form['inputPassword']

    #     # validate the received values
    #     if _name and _email and _password:

    #         # All Good, let's call MySQL


    #         _hashed_password = generate_password_hash(_password)
    #         cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
    #         data = cursor.fetchall()

    #         if len(data) is 0:
    #             conn.commit()
    #             return json.dumps({'message':'User created successfully !'})
    #         else:
    #             return json.dumps({'error':str(data[0])})
    #     else:
    #         return json.dumps({'html':'<span>Enter the required fields</span>'})

    # except Exception as e:
    #     return json.dumps({'error':str(e)})
    # finally:
    #     cursor.close()
    #     conn.close()
def adduser():
    print "Entered"
    try:
        name = request.form['inputName']
        password = request.form['inputPassword']
        print name,password
        cursor.execute("INSERT INTO users (username, password) VALUES (%s,%s)",(name, password))
        db.commit()
        print "Registered"
    except Exception as e:
       return(str(e))
    return

if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
