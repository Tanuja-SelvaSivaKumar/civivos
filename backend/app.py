from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="CivicOS",
    version="1.0.0",
    description="Autonomous Civic Workflow Engine"
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "Welcome to CivicOS API"
    }