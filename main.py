import importlib
from fastapi import FastAPI
from app.core.config import settings

# Create FastAPI app instance
app = FastAPI(
    title="CGCG API",
    description="API for CGCG services",
    version="1.0.0",
)

def register_routers(app: FastAPI):
    """
    Registers routers from modules specified in the MODULES config.
    """
    print("Loading modules based on configuration...")
    for module_config in settings.MODULES:
        if not module_config.enabled:
            print(f"Skipping disabled module: {module_config.name}")
            continue
        
        try:
            # The import path to the router.py file
            router_import_path = f"{module_config.path}.router"
            
            print(f"Attempting to load router from: {router_import_path}")
            
            # Dynamically import the router.py file from the specified path
            router_module = importlib.import_module(router_import_path)
            router = getattr(router_module, "router", None)
            
            if router:
                app.include_router(router)
                print(f"Successfully registered router from module: {module_config.name} (path: {module_config.path})")
            else:
                print(f"Warning: Module '{module_config.name}' is enabled but no 'router' instance was found in {router_import_path}.")
        except ImportError as e:
            print(f"Error: Could not import router from enabled module '{module_config.name}'. Details: {e}")

# Register all routers from the modules directory
register_routers(app)

@app.get("/", tags=["Default"])
async def root():
    """
    Root endpoint for health check.
    """
    return {"message": "Welcome to CGCG API"}

# The following is for running the app with uvicorn when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
