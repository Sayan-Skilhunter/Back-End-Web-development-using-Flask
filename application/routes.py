from application import app, db
from application.models import User, Course, Enrollment
from flask import render_template, request, Response, json, redirect, flash
from application.forms import LoginForm, RegisterForm

CourseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, 
            {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, 
            {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, 
            {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, 
            {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index = True)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        email = form.email.data
        password = form.password.data
        user = User.objects(email = email).first()
        
        if user and password == user.password:
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong", "danger")
    return render_template("login.html", form = form, title = "Login", login = True)

@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = "Spring 2019"):
    return render_template("courses.html", CourseData = CourseData, courses = True, term = term)

@app.route("/register")
def register():
    return render_template("register.html", register = True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term = request.form.get('term')
    return render_template("enrollment.html", data = { "id":id, "title":title, "term":term })

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx = None):
    if idx == None:
        jdata = CourseData
    else:
        jdata = CourseData[int(idx)-1]

    return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    #User(user_id = 1, first_name = "Sayan", last_name = "Sen", email = "sayansen2507@gmail.com", password = "abc1234").save()
    #User(user_id = 2, first_name = "Mary", last_name = "Jane", email = "mary.jane@uta.com", password = "pass123").save()
    users = User.objects.all()
    return render_template("user.html", users = users)
    