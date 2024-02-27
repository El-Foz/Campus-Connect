import os, sqlite3, jwt
from flask import Flask, render_template, request, redirect, session, make_response
app=Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
from dotenv import load_dotenv
load_dotenv()
db = sqlite3.connect("database.db", check_same_thread=False)
jwtkey=os.environ['jwtkey']
app.secret_key = os.environ["key"]
@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/signup')
def signup():
    return render_template("signup.html")
@app.route("/signup/teacher")
def signupteacher():
    return render_template('/signupteach.html')

@app.route('/signup/student')
def signupstudent():
    return render_template('/signupstud.html')

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/login/teacher')
def loginteach():
    return render_template('/loginteach.html')

@app.route('/login/student')
def loginstudent():
    return render_template('/loginstud.html')
 
@app.route("/signupcomplete/stud", methods=['POST'] )
def completestud():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO USERS (USERNAME, PW, EMAIL, NAME, STUDENT) values (?, ?, ?,?, ?)",[
            request.form['username'],
            request.form["password"],
            request.form['email'],
            request.form['first'] + " " + request.form['last'],
            1 # student
        ])
        return redirect("/")
@app.route("/studpage")
def sdfghj():
    render_template("studpage.html")
@app.route('/logincomplete/stud', methods=["POST"])
def logincompletestud():
    with sqlite3.connect("database.db") as con:
        cur=con.cursor()
        res=cur.execute("SELECT * FROM USERS")
        z=res.fetchall()
        n=False
        resp=make_response(redirect("/teacher/schedule"))
        for i in z:
            if i[1] == request.form['username'] and request.form['password']==i[2]:
                n=True
                break
        if n:
            token=jwt.encode(
                {'data': i},
                jwtkey, 
                algorithm='HS256'
            )
            print(token)
            resp.set_cookie('user', token)
        return resp


        return resp
@app.route('/teacher/schedule')
def teacherschedule():
    cooking=request.cookies.get("user")
    print(cooking)
    if cooking != None:
        x=jwt.decode(cooking, os.environ["jwtkey"], algorithms=['HS256', ])
        print(cooking)
        return render_template("teachersched.html")
    return "not logged in"

@app.route("/submiteachersched",methods=["POST"])
def submitteachersstuff():
    with sqlite3.connect("database.db") as con:
        cur=con.cursor()

@app.route("/home")
def poiuytr():
    return redirect("/")
@app.route('/logincomplete/teach',methods =["POST"])
def logincompleteteach():
    with sqlite3.connect("database.db") as con:
        cur=con.cursor()
        res=cur.execute("SELECT * FROM USERS")
        z=res.fetchall()
        n=False
        resp=make_response(redirect("/teacher/schedule"))
        for i in z:
            if i[1] == request.form['username'] and request.form['password']==i[2]:
                n=True
                break
        if n:
            token=jwt.encode(
                {'data': i},
                jwtkey, 
                algorithm='HS256'
            )
            print(token)
            resp.set_cookie('user', token)
        return resp


@app.route("/signupcomplete/teach", methods=['POST'] )
def completeteach():
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO USERS (USERNAME, PW, EMAIL, NAME, STUDENT) values (?, ?, ?,?, ?)", [
            request.form['username'],
            request.form["password"],
            request.form['email'],
            request.form['first']+" "+request.form['last'], 
            0 # teacher
        ])
        db.commit()
        return redirect("/")


if __name__ == '__main__':
    app.run()