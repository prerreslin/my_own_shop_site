from ..app import app, BACKEND_URL
from flask import render_template, request, redirect, url_for
from requests import get,post
from flask_login import current_user


@app.get("/bag")
def bag():
    if not current_user.is_authenticated:
        return redirect(url_for("get_email"))
    return render_template("bag.html", user=current_user)