from fastapi import FastAPI

from app.projects.router import router

APP_NAME = "Board API"
APP_VERSION = "0.1.0"


app = FastAPI(title=APP_NAME, version=APP_VERSION, description="This is Board Api")
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def get_service_info():
    return {"name": APP_NAME, "version": APP_VERSION, "docs": "/docs"}
