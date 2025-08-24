import sys
import os
from fastapi import FastAPI
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.packet_sniffer import sniffer
from app.routes import router
from app.utils import print_banner, simulate_system_startup

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Cyber Threat Dashboard",
    description="Real-time network threat detection system",
    version="1.0.0"
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Start services on application startup"""
    print_banner()
    simulate_system_startup()
    
    # Start packet sniffer in background thread
    sniffer.start()
    print("📡 Packet sniffer started in background thread")

@app.get("/")
def read_root():
    return {
        "message": "AI Cyber Threat Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "threats": "/api/v1/threats",
            "stats": "/api/v1/threats/stats"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "sniffing": sniffer.running,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🌐 Starting web server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)