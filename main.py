from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles
from app.routers import agent_router
from app.websocket.router import router as websocket_router

# Initialize FastAPI app
app = FastAPI(
    title="My AI Assistant",
    description="A simple FastAPI application",
    version="0.1.0"
)

# Include routers
app.include_router(agent_router)
app.include_router(websocket_router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    """
    Root endpoint that returns basic app information.
    """
    return {
        "app": "FastAPI Application",
        "status": "Running",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    # Run the application with uvicorn when this file is executed directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

