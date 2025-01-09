from ..app import app, BACKEND_URL
from flask import render_template, request
from flask_login import current_user
from requests import get
from datetime import datetime, timedelta

@app.get("/cloth-type")
def cloth_type():
    type_of = request.args.get("type")
    clothing = request.args.get("clothing")
    response = []
    if clothing == "All":
        response = get(f"{BACKEND_URL}/api/shop/get_all_clothing").json()
        if type_of == "New":
            thirty_days_ago = datetime.now() - timedelta(days=30)
            response = [
                item for item in response
                if "created_at" in item and datetime.fromisoformat(item["created_at"]) >= thirty_days_ago
            ]

    else:
        response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_type?type_of={type_of}").json()

    if type_of == "Men's" or type_of == "Woman's":
        response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_gender?gender={type_of}").json()
        
    if current_user.is_authenticated:
        return render_template("cloth-type.html",user=current_user,clothes=response,type_of=type_of,clothing=clothing)
    return render_template("cloth-type.html",clothes=response,type_of=type_of,clothing=clothing)