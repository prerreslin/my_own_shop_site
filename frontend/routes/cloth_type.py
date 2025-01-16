from ..app import app, BACKEND_URL
from flask import render_template, request, redirect, url_for
from flask_login import current_user
from requests import get
from datetime import datetime, timedelta

@app.get("/cloth-type")
def cloth_type():
    type_of = request.args.get("type")
    clothing = request.args.get("clothing")
    response = []

    if clothing == "All":
        if type_of == "Men's" or type_of == "Woman's" or type_of == "Kid's":
            response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_gender?gender={type_of}").json()
            if type(response) == dict:
                response = []
        if type_of == "New":
            response = get(f"{BACKEND_URL}/api/shop/get_all_clothing").json()
            thirty_days_ago = datetime.now() - timedelta(days=30)
            response = [
                item for item in response
                if "created_at" in item and datetime.fromisoformat(item["created_at"]) >= thirty_days_ago
            ]
        if type_of == "Favourite":
            if current_user.is_authenticated:
                response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_favourite?user_id={current_user.id}").json()
                if type(response) == dict:
                    response = []
            else:
                return redirect(url_for("get_email"))
        if type_of == "Jordan's":
            response = get(f"{BACKEND_URL}/api/shop/get_jordans").json()
        if type_of == "Sale":
            response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_sale").json()
    else:
        response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_type?type_of={type_of}").json()
        if type(response) == dict:
            response = []

    if current_user.is_authenticated:
        return render_template("cloth-type.html",user=current_user,clothes=response,type_of=type_of,clothing=clothing)
    return render_template("cloth-type.html",clothes=response,type_of=type_of,clothing=clothing)


@app.get("/search")
def search():
    query = request.args.get('q', '')
    response = get(f"{BACKEND_URL}/api/shop/search_clothing?search={query}").json()
    type_of = ""
    if type(response) != dict:
        type_of = response[0]["name_of_clothes"]
    else:
        response = []

    if current_user.is_authenticated:
        return render_template("cloth-type.html",user=current_user,type_of=query,clothes=response,clothing="All",search=query)
    return render_template("cloth-type.html",clothes=response,search=query,type_of=query,clothing="All")