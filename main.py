# main.py

from fastapi import FastAPI
from app.api.endpoints import deadline, scans, syncs

app = FastAPI()

app.include_router(deadline.router)
app.include_router(scans.router)
app.include_router(syncs.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI app for Deadline job queries"}
