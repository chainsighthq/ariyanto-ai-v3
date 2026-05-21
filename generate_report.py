import subprocess
from datetime import datetime
from pathlib import Path

def generate_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{'='*60}")
    print(f"ARIYANTO AI v3 - SYSTEM REPORT")
    print(f"Generated: {timestamp}")
    print(f"{'='*60}\n")
    
    # Check service status
    try:
        result = subprocess.run(["systemctl", "is-active", "ariyanto-ai"], capture_output=True, text=True)
        service_status = result.stdout.strip()
        print(f"Service Status: {service_status.upper()}")
    except:
        print("Service Status: UNKNOWN")
    
    # Check Redis
    try:
        result = subprocess.run(["redis-cli", "ping"], capture_output=True, text=True)
        redis_status = "OK" if "PONG" in result.stdout else "DOWN"
        print(f"Redis Status: {redis_status}")
    except:
        print("Redis Status: UNKNOWN")
    
    # Check disk space
    try:
        result = subprocess.run(["df", "-h", "/home/ubuntu/ariyanto-ai-v3"], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            print(f"Disk Usage: {lines[1].split()[4]}")
    except:
        pass
    
    # Check backup
    backup_dir = Path("backups")
    if backup_dir.exists():
        backups = list(backup_dir.iterdir())
        print(f"Backups: {len(backups)} available")
        if backups:
            latest = max(backups, key=lambda x: x.stat().st_mtime)
            print(f"Latest Backup: {latest.name}")
    
    print(f"\n{'='*60}")
    print("Report generated successfully!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    generate_report()
