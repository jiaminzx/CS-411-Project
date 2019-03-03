from flask import Flask, render_template
app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi
 
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/main")
def m():
    return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():  
    return render_template('index2.html')

###remove below if wsgi
if __name__ == "__main__":
    app.run()