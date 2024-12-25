import os
from flask import Flask
from asgiref.wsgi import WsgiToAsgi
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
BACKEND_URL = os.getenv("BACKEND_URL")

app = Flask(__name__, template_folder="templates")
app.secret_key = SECRET_KEY
asgi_app = WsgiToAsgi(app)

from . import routes