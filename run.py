import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Cyber Threat Detection Server...")
    print("🌐 Open: http://localhost:8000")
    print("📊 API Docs: http://localhost:8000/docs")
    print("🛑 Press CTRL+C to stop")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)