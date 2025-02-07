from ..app import app, BACKEND_URL
from ..forms import EmailForm,RegisterForm, LoginForm
from ..db.models import User
from flask import render_template, redirect, url_for, request
from flask_login import login_user, LoginManager, logout_user
from requests import get, post

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    response = get(f"{BACKEND_URL}/api/user/get_user_by_id?user_id={user_id}")
    if response.status_code == 200:
        return User(response.json())



@app.get("/email")
def get_email():
    form = EmailForm()
    return render_template("email.html",form=form)


@app.post("/email")
def post_email():
    form = EmailForm()

    if form.validate_on_submit():
        email = form.email.data
        response = get(f"{BACKEND_URL}/api/user/get_user_by_email?email={email}").json()
        if response.get("status") == "register":
            return redirect(url_for("register",email=email))
        return redirect(url_for("login",email=email))
    

@app.get("/register")
def register():
    form = RegisterForm()
    form.email.data = request.args.get("email")
    return render_template("register.html",form=form)


@app.post("/register")
def post_register():
    form = RegisterForm()

    if form.validate_on_submit():
        data = {
            "username": form.username.data,
            "password": form.password.data,
            "email": form.email.data
        }
        response = post(f"{BACKEND_URL}/api/user/register",json=data)
        if response.status_code == 200:
            user_data = response.json()
            user = User(user_data)
            login_user(user)
            return redirect(url_for("index"))
        if response.status_code == 422:
            error = response.json().get("detail", "Unknown error")[0].get("msg")
            error = error.replace("Value error,", "")
            error = error.replace("String", "")
            return render_template("register.html", form=form, error=error)
    else:
        return render_template("register.html", form=form)
    

@app.get("/login")
def login():
    form = LoginForm()
    form.email.data = request.args.get("email")
    return render_template("login.html",form=form)


@app.post("/login")
def post_login():
    form = LoginForm()

    if form.validate_on_submit():
        print(form.email.data, form.password.data) 
        data = {
            "password": form.password.data,
            "email": form.email.data
        }
        response = post(f"{BACKEND_URL}/api/user/login",json=data)
        if response.status_code == 200:
            user_data = response.json()
            user = User(user_data)
            login_user(user)
            return redirect(url_for("index"))
        else:
            error = response.json().get("detail", "Unknown error")
            return render_template("login.html", form=form, error=error)
            
            
    else:
        return render_template("login.html", form=form)
    

@app.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))