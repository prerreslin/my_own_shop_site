from uvicorn import run
from backend.app import app

if __name__ == "__main__":
    run("backend.app:app", host="127.0.0.1", port=8000, reload=True)