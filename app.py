from flask import Flask, render_template, json,jsonify, request
#import MySQL
import mysql.connector as mariadb



app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/showUsers")
def showUsers():
    mariadb_connection = mariadb.connect(user='username', password='password', database='cs411project')
    cursor = mariadb_connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    return jsonify(rows)
    mariadb_connection.close()


@app.route('/showSignUp')
def signUp():
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

if __name__ == "__main__":
    app.run(host='sp19-cs411-36.cs.illinois.edu', port=8081)
