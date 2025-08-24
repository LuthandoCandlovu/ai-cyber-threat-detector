#!/usr/bin/env python3
"""
🚀 AI Cybersecurity Threat Detection System
Main entry point for the application
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"📁 Current directory: {current_dir}")
print(f"📦 Python path: {sys.path}")

def main():
    """Main function to start the threat detection system"""
    try:
        print("🔐" * 50)
        print("🚀 STARTING CYBERSECURITY THREAT DETECTION SYSTEM")
        print("🔐" * 50)
        
        # Check if app folder exists
        app_dir = os.path.join(current_dir, 'app')
        if not os.path.exists(app_dir):
            print(f"❌ ERROR: app folder not found at {app_dir}")
            print("📁 Files in current directory:")
            for file in os.listdir(current_dir):
                print(f"   - {file}")
            return
        
        print(f"✅ Found app folder at: {app_dir}")
        
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