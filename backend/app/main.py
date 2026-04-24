"""
FastAPI application entry point for VitalTriage backend.
"""
import logging
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables from .env file
load_dotenv()

from app.db import mongo
from app.routes import patient_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting up VitalTriage API...")
    try:
        await mongo.connect_to_mongo()
        if mongo.db is not None:
            logger.info("✓ MongoDB connection established")
        else:
            logger.warning("⚠️  Running in DEMO MODE - MongoDB unavailable")
    except Exception as e:
        logger.error(f"MongoDB connection error: {str(e)}")
        logger.warning("⚠️  Continuing in DEMO MODE - data will be stored in memory")
    
    yield
    
    # Shutdown
    logger.info("Shutting down VitalTriage API...")
    await mongo.close_mongo_connection()
    logger.info("MongoDB connection closed")


# Create FastAPI app
app = FastAPI(
    title="VitalTriage API",
    description="AI Patient Monitoring System - Backend API for vital signs assessment and risk scoring",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(patient_routes.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to VitalTriage API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
