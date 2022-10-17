import uvicorn

from api import create_app, settings

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app=app, host=settings.fastapi_app, port=settings.fastapi_port)
