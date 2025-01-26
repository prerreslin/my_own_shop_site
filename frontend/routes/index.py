from ..app import app
from flask import render_template
from flask_login import current_user

@app.get("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html",user=current_user)
    return render_template("index.html")


@app.get("/nav")
def nav():
    return render_template("__navbar.html")