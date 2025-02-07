from ..app import app, BACKEND_URL
from flask import render_template
from flask_login import current_user
from requests import get



@app.get('/gift_cards')
def gift_cards():
    cards = get(f"{BACKEND_URL}/api/gift_cards/get_all").json()
    if not current_user.is_authenticated:
        return render_template('gift-cards.html', user=current_user,cards=cards)
    return render_template('gift-cards.html',cards=cards)