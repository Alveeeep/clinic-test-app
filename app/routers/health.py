from fastapi import APIRouter


health_router = APIRouter(tags=["Application Healthcheck"])

@health_router.get("/health")
async def healthcheck():
    return {'status': 'ok'}
