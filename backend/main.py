from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager
from app.api.endpoints import router as api_router
from app.mcp.client_manager import mcp_manager
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (StarletteHTTPException, Exception) as e:
            index_path = os.path.join(self.directory, "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path, status_code=200)
            raise e

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    Initializes MCP connections on startup.
    """
    logger.info("Starting up CipherEye API...")
    await mcp_manager.initialize_all()
    yield
    logger.info("Shutting down CipherEye API...")

def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    app = FastAPI(
        title="CipherEye API",
        description="Backend API for the CipherEye AI-powered cyber investigation platform.",
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS Middleware (Allow frontend to connect)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the main API router
    app.include_router(api_router)

    @app.get("/health")
    async def health_check():
        """Basic health check endpoint."""
        return {"status": "healthy", "service": "CipherEye API"}

    # Serve static frontend files if they exist (for production/Docker deployment)
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"),
        os.path.join(os.path.dirname(__file__), "frontend", "dist"),
        "/app/frontend/dist",
        "frontend/dist",
        "/home/user/app/frontend/dist"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Serving static frontend files from: {path}")
            app.mount("/", SPAStaticFiles(directory=path, html=True), name="frontend")
            break

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Run the application locally
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# Trigger reload: verified correct key added
