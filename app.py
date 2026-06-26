from flask import Flask, render_template, request, redirect, send_file, session
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    UserMixin
)

import sqlite3
import requests
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader



app = Flask(__name__)

app.secret_key="secret123"


bcrypt=Bcrypt(app)


login_manager=LoginManager(app)
login_manager.login_view="login"





# DATABASE

def db():
    return sqlite3.connect("database.db")



def init_db():

    con=db()
    c=con.cursor()


    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
    )
    """)



    c.execute("""
    CREATE TABLE IF NOT EXISTS leaderboard(
    username TEXT UNIQUE,
    score INTEGER
    )
    """)


    con.commit()
    con.close()



init_db()







class User(UserMixin):

    def __init__(self,id,username):

        self.id=id
        self.username=username






@login_manager.user_loader
def load_user(id):

    con=db()
    c=con.cursor()


    c.execute(
        "SELECT * FROM users WHERE id=?",
        (id,)
    )


    user=c.fetchone()

    con.close()


    if user:

        return User(
            user[0],
            user[1]
        )









# REGISTER

@app.route("/register",methods=["GET","POST"])
def register():


    if request.method=="POST":


        username=request.form["username"]


        password=bcrypt.generate_password_hash(
            request.form["password"]
        ).decode()



        con=db()

        c=con.cursor()



        try:

            c.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (username,password)
            )

            con.commit()


        except:

            pass



        con.close()


        return redirect("/login")



    return render_template("register.html")











# LOGIN


@app.route("/login",methods=["GET","POST"])
def login():


    if request.method=="POST":


        username=request.form["username"]

        password=request.form["password"]



        con=db()

        c=con.cursor()



        c.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
        )


        user=c.fetchone()


        con.close()




        if user:


            if bcrypt.check_password_hash(
                user[2],
                password
            ):


                login_user(
                    User(
                        user[0],
                        user[1]
                    )
                )


                return redirect("/")



    return render_template("login.html")









@app.route("/logout")
def logout():

    logout_user()

    return redirect("/login")











# GITHUB ANALYSIS


def analyze(username):


    user=requests.get(
        f"https://api.github.com/users/{username}"
    ).json()



    repos=requests.get(
        f"https://api.github.com/users/{username}/repos"
    ).json()





    score=(

        user.get("public_repos",0)*8

        +

        user.get("followers",0)*2

    )


    score=min(score,100)





    languages=[]



    for repo in repos:


        if repo.get("language"):

            languages.append(
                repo.get("language")
            )



    languages=list(set(languages))





    return {


    "username":username,


    "avatar":user.get("avatar_url"),


    "bio":
    user.get("bio") or "No bio available",


    "location":
    user.get("location") or "Not mentioned",


    "company":
    user.get("company") or "Not mentioned",


    "github":
    f"https://github.com/{username}",


    "repos":
    user.get("public_repos",0),


    "followers":
    user.get("followers",0),


    "stars":0,


    "score":score,


    "languages":languages,



    "suggestions":[

        "Add README files",

        "Improve project documentation",

        "Create more projects"

    ]


    }











# HOME


@app.route("/",methods=["GET","POST"])
@login_required
def index():


    result=None



    if request.method=="POST":


        username=request.form["username"]


        result=analyze(username)



        session["report"]=result




        con=db()

        c=con.cursor()



        c.execute(
        """
        INSERT INTO leaderboard(username,score)
        VALUES(?,?)

        ON CONFLICT(username)
        DO UPDATE SET score=excluded.score
        """,
        (
        username,
        result["score"]
        )
        )



        con.commit()

        con.close()





    con=db()

    c=con.cursor()



    c.execute(
    """
    SELECT username,score
    FROM leaderboard
    ORDER BY score DESC
    LIMIT 5
    """
    )


    leaderboard=c.fetchall()


    con.close()





    return render_template(
        "index.html",
        result=result,
        leaderboard=leaderboard
    )













# PDF DOWNLOAD


@app.route("/download")
@login_required
def download():


    data=session.get("report")



    if not data:

        return "Analyze profile first"




    path="github_report.pdf"



    pdf=canvas.Canvas(
        path,
        pagesize=letter
    )


    width,height=letter



    y=750





    pdf.setFont(
        "Helvetica-Bold",
        22
    )


    pdf.drawString(
        170,
        y,
        "GitHub Analyzer Report"
    )


    y-=40






    try:


        img=ImageReader(
            data["avatar"]
        )


        pdf.drawImage(
            img,
            220,
            y-120,
            width=120,
            height=120
        )


        y-=150


    except:

        pass





    pdf.setFont(
        "Helvetica",
        13
    )





    details=[


    "Username : "+data["username"],

    "Bio : "+data["bio"],

    "Location : "+data["location"],

    "Company : "+data["company"],

    "GitHub : "+data["github"],


    "",


    "Recruiter Score : "+str(data["score"])+"%",


    "",


    "Repositories : "+str(data["repos"]),


    "Followers : "+str(data["followers"]),


    "Stars : "+str(data["stars"]),


    "",


    "Languages : "+", ".join(data["languages"]),


    "",


    "AI Suggestions"


    ]






    for line in details:


        pdf.drawString(
            70,
            y,
            line
        )


        y-=25





    for s in data["suggestions"]:


        pdf.drawString(
            90,
            y,
            "✓ "+s
        )


        y-=25





    pdf.save()




    return send_file(
        path,
        as_attachment=True
    )









if __name__=="__main__":


    app.run(debug=True)