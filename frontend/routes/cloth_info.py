from ..app import app, BACKEND_URL
from flask import render_template, request
from requests import get

@app.get("/cloth-info")
def cloth_info():
    id = request.args.get("id")
    response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_id?id={id}").json()
    return render_template("cloth-info.html", clothing=response)