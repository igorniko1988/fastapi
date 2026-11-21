from fastapi import FastAPI

app = FastAPI(title="Board Api", version="1.0", description="This is Board Api")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
def get_app_version():
    return {"name": "Board API", "version": "0.1.0"}
