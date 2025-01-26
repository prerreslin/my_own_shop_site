from ..app import app, BACKEND_URL
from flask import render_template, request, redirect, url_for
from requests import get,post
from flask_login import current_user

@app.get("/cloth-info")
def cloth_info():
    gift = request.args.get("gift")
    if gift:
        responce = get(f"{BACKEND_URL}/api/gift_cards/get_by_id?id={gift}").json()
        print(responce)
        if not responce["name"]:
            return redirect(url_for("gift_cards"))
        return render_template("cloth-info.html", clothing=responce)
    id = request.args.get("id")
    favourite = request.args.get("favourite")
    response = get(f"{BACKEND_URL}/api/shop/get_all_clothing_by_id?id={id}").json()
    if favourite == "true":
        if current_user.is_authenticated:
            if get(f"{BACKEND_URL}/api/shop/check_for_favourite?shop_id={response['data']['id']}&user_id={current_user.id}").json() == {"data":"false"}:
                post(f"{BACKEND_URL}/api/shop/add_favourite?user_id={current_user.id}&shop_id={response['data']['id']}")
                return redirect(url_for("cloth_info",id=id))
            else:
                return redirect(url_for("cloth_info",id=id))
        else:
            return redirect(url_for("get_email"))
    if current_user.is_authenticated:
        if get(f"{BACKEND_URL}/api/shop/check_for_favourite?shop_id={response['data']['id']}&user_id={current_user.id}").json() == {"data":"true"}:
            return render_template("cloth-info.html", clothing=response["data"],favourite="true")

    return render_template("cloth-info.html", clothing=response["data"])