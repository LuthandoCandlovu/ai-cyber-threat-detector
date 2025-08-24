#!/usr/bin/env python3
"""
🚀 AI Cybersecurity Threat Detection System
Main entry point for the application
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to start the threat detection system"""
    try:
        print("🔐" * 50)
        print("🚀 STARTING CYBERSECURITY THREAT DETECTION SYSTEM")
        print("🔐" * 50)
        
        # Import and start the main application
        from app.main import app
        import uvicorn
        
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 Web Dashboard: http://localhost:8000")
        print("📊 API Health: http://localhost:8000/health")
        print("📋 API Docs: http://localhost:8000/docs")
        print("🔐" * 50)
        print("Press CTRL+C to stop the system...")
        
        # Start the web server
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down threat detection system...")
        print("✅ All systems secured. Goodbye! 👋")
    except Exception as e:
        print(f"❌ Error starting system: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()