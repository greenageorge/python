from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3
import hashlib
K = 'user.db'
app = Flask(__name__)

def validate(username, password):
    con = sqlite3.connect(K)
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT USERNAME,PASSWORD from Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username:
                       if dbPass==password:
                        completion=True
                       else:
                        completion=False
                    else:
                        completion=-1
    return completion


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username,password)
        if completion ==False:
            return render_template('login.html', msg="invalid")
        if completion == True:
            return ("Successfully logged in!")
        if completion == -1:
            return redirect('/signup')
    else:
     return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
 if request.method == 'POST': 
   username = request.form['username']
   password = request.form['password']
   con = sqlite3.connect("user.db")
   cur = con.cursor()
   cur.execute("INSERT INTO Users (USERNAME,PASSWORD) VALUES (?,?)", (username,password))
   con.commit()
   con.close()
   return redirect('/')
 else:
   return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
