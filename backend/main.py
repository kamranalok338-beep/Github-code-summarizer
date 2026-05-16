from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.api.routes import router as api_router

# Initialize the core FastAPI instance with the new project branding
app = FastAPI(
    title="GitHub Code Summarizer API",
    description="An Enterprise-grade AI pipeline that converts GitHub repositories into comprehensive technical summaries.",
    version="1.0.0"
)

# Standard Cross-Origin Resource Sharing (CORS) setup for secure frontend messaging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering application routers with API prefix rules
app.include_router(api_router, prefix="/api")

@app.get("/")
def health_check():
    """Simple microservice health probe endpoint."""
    return {"status": "Online", "message": "GitHub Code Summarizer API is fully operational."}

if __name__ == "__main__":
    print("[INFO] Starting Uvicorn deployment server for GitHub Code Summarizer...")
    # Running the service on local network loopback port 8000
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)