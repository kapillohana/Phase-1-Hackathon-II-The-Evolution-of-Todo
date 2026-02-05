"""
Main entry point for the Advanced Todo Application backend
Sets up the FastAPI application and includes all API routes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.main import router as api_router
from .api.auth import router as auth_router
from .database.database import create_db_and_tables
import os

# Create the main FastAPI application
app = FastAPI(
    title="Advanced Todo API",
    description="REST API for the Advanced Todo Application with authentication and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api", tags=["api"])
# Include authentication routes
app.include_router(auth_router, prefix="", tags=["authentication"])  # No prefix since auth router already has /auth prefix

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Advanced Todo API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "OK", "phase": "2_complete"}

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )