from ..app import app, BACKEND_URL
from ..forms import EmailForm,RegisterForm, LoginForm
from flask import render_template, redirect, url_for, request
from flask_login import login_user
from requests import get, post



@app.get("/email")
def get_email():
    form = EmailForm()
    return render_template("email.html",form=form)


@app.post("/email")
def post_email():
    form = EmailForm()

    if form.validate_on_submit():
        email = form.email.data
        responce = get(f"{BACKEND_URL}/api/user/get_user_by_email?email={email}").json()
        if responce.get("status") == "register":
            return redirect(url_for("register",email=email))
        return redirect(url_for("login"),email=email)
    

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
        responce = post(f"{BACKEND_URL}/api/user/register",json=data)
        if responce.status_code == 200:
            return responce.text
        if responce.status_code == 422:
            error = responce.json().get("detail", "Unknown error")[0].get("msg")
            return render_template("register.html", form=form, error=error)
    else:
        return render_template("register.html", form=form)
    

@app.get("/login")
def login():
    form = LoginForm()
    form.email.data = request.args.get("email")
    return render_template("login.html",form=form)


#TODO: POST /login

# @app.post("/login")
# def post_login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         data = {
#             "password": form.password.data,
#             "email": form.email.data
#         }
#         responce = post(f"{BACKEND_URL}/api/user/login",json=data)
#         if responce.status_code == 200:
#             return responce.text
#         else:
            
            
#     else:
#         return render_template("login.html", form=form)