from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="Civivos AI"
)


app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
def home():

    return {
        "message": "Civivos AI running"
    }