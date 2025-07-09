from fastapi import FastAPI
from app.routers.appointments import router
from app.routers.health import health_router

app = FastAPI()

app.include_router(router)
app.include_router(health_router)
