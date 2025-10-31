# Main router for API v1
from fastapi import APIRouter

# Import module routers
from app.modules.deadline.routers import module_router as deadline_router
from app.modules.media_shuttle.router import router as media_shuttle_router
from app.api.v1.endpoints import users as v1_users_router

api_router = APIRouter()

# Include module routers
api_router.include_router(v1_users_router.router)
api_router.include_router(deadline_router)
api_router.include_router(media_shuttle_router)


# You can also include other v1-specific endpoints here in the future
# from .endpoints import some_other_endpoint
# api_router.include_router(some_other_endpoint.router, prefix="/other", tags=["Other"])