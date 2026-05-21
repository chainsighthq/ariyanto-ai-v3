import subprocess
import time
from datetime import datetime

def check_status():
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "ariyanto-ai"],
            capture_output=True, text=True
        )
        status = result.stdout.strip()
        
        print(f"\n{'='*50}")
        print(f"ARIYANTO AI v3 - Status Monitor")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        print(f"Service Status: {status.upper()}")
        
        if status == "active":
            print("✅ Production AI is running normally")
        else:
            print("❌ Production AI is NOT running")
            print("Run: sudo systemctl restart ariyanto-ai")
        
        print(f"{'='*50}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_status()
