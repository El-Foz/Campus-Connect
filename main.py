import os, sqlite3, jwt
from flask import Flask, render_template, request, redirect, session, make_response
app=Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
from dotenv import load_dotenv
load_dotenv()
db = sqlite3.connect("database.db")

app.secret_key = os.environ["key"]
jwtkey=os.environ["jwtkey"]
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
 
@app.route("/signupcomplete/student", methods=['POST'] )
def completestud():
    cur = db.cursor()
    cur.execute("INSERT INTO USERS (USERNAME, PW, EMAIL,  STUDENT) values (?, ?, ?, ?))",[
        request.form['username'],
        request.form['email'],
        hash(request.form["password"]),
        request.form['first'] + " " + request.form['last'],
        1 # student
    ])
    redirect("/")

@app.route('/logincomplete/stud', methods=["POST"])
def logincompletestud():
    with sqlite3.connect("database.db") as con:
        res=con.cursor().execute("SELECT * FROM USERS")
        res.fetchall()
        x=0
        n=False
        for i in res:
            if i[1]==request.form['username'] and hash(request.form['password'])==i[3]:
                n=True
                break
            x+=1
        if n:
            token=jwt.encode(
                payload=res[x],
                key=jwtkey
            )
            resp=make_response("test")
            resp.set_cookie('user', token)

        return "test"
@app.route('/teacher/schedule')
def teacherschedule():
    return render_template("teachersched.html")
@app.route('/logincomplete/teach',methods =["POST"])
def logincompleteteach():
    with sqlite3.connect("database.db") as con:
        cur=con.cursor()
        res=cur.execute("SELECT * FROM USERS")
        res.fetchall()
        x=0
        n=False
        for i in res:
            if i[1] == request.form['username'] and hash(request.form['password'])==i[3]:
                n=True
                break
            x+=1
        if n:
            token=jwt.encode(
                payload=res[x]
            )

        return "test"

    #return "teacher login"

@app.route("/signupcomplete/teach", methods=['POST'] )
def completeteach():
    cur = db.cursor()
    cur.execute("INSERT INTO USERS (USERNAME, PW, EMAIL,  TEACHER) values (?, ?, ?, ?))",[
        request.form['username'],
        request.form['email'],
        hash(request.form["password"]),
        request.form['first']+" "+request.form['last'], 
        0 # teacher
    ])
    db.commit()
    redirect("/")

if __name__ == '__main__':
    app.run()