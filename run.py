import asyncio
from uvicorn import Server, Config

async def run_backend():
    server = Server(Config("backend.app:app", host="127.0.0.1", port=8000, reload=True))
    await server.serve()

async def run_frontend():
    server = Server(Config("frontend.app:asgi_app", host="127.0.0.1", port=5000, reload=True))
    await server.serve()

async def main():
    await asyncio.gather(run_backend(), run_frontend())

if __name__ == "__main__":
    asyncio.run(main())