import subprocess
from datetime import datetime

def show_log(lines=20):
    try:
        result = subprocess.run(
            ["tail", "-n", str(lines), "logs/production.log"],
            capture_output=True, text=True
        )
        
        print(f"\n{'='*60}")
        print(f"ARIYANTO AI v3 - Production Log (Last {lines} lines)")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        print(result.stdout)
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_log(30)
