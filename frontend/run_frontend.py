import os
from flask import Flask

app = Flask(__name__, template_folder=os.path.join("frontend", "templates"))

import routes

if __name__ == "__main__":
    app.run(port=5000)