from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/root")
def get_app_version():
    return {"name": "Board API", "version": "0.1.0"}
