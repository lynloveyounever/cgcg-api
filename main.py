from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from app.api.v1.api_router import api_router as api_v1_router

# Create FastAPI app instance
app = FastAPI(
    title="CGCG API",
    description="A comprehensive API for CGCG services",
    version="1.0.0",
)

mcp = FastApiMCP(
    app,
    include_tags=["Deadline AI Tools"]  # Only include AI tools endpoints in MCP
)
mcp.mount() # 預設會在 /mcp 創建服務

# Include the versioned API router
# All application routes are now managed in api_router.py
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/", tags=["Default"])
async def root():
    """
    Root endpoint for health check.
    """
    return {"message": "Welcome to CGCG API. All endpoints are available under /api/v1"}


# The following is for running the app with uvicorn when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")