# main.py

from fastapi import FastAPI
from app.api.routers import deadline_router, user_router
from app.utils.logging_utils import setup_logging
import logging

# Setup logging early
setup_logging(level=logging.INFO, log_file="app.log") # Or logging.DEBUG for development

app = FastAPI()

app.include_router(deadline_router.router)
app.include_router(user_router.router)

@app.get("/")
def read_root():
    logger = logging.getLogger(__name__) # Get logger for main module
    logger.info("Root endpoint accessed.")
    return {"message": "FastAPI app for Deadline job queries"}
