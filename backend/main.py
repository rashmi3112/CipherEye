from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager
from app.api.endpoints import router as api_router
from app.mcp.client_manager import mcp_manager

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

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Run the application locally
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
# Trigger reload: verified correct key added
